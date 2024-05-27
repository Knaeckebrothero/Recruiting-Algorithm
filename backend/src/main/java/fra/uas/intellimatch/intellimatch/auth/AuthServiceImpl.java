package fra.uas.intellimatch.intellimatch.auth;


import fra.uas.intellimatch.intellimatch.auth.dto.AuthRequestDto;
import fra.uas.intellimatch.intellimatch.auth.dto.RegistrationRequestDto;
import fra.uas.intellimatch.intellimatch.model.User;
import fra.uas.intellimatch.intellimatch.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthServiceImpl implements AuthService {
    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;
    private final InMemoryUserDetailsService userDetailsService;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public Map<String, String> authRequest(AuthRequestDto authRequestDto) {
        final var authenticate = authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(authRequestDto.userName(), authRequestDto.password()));
        final var userDetails = (UserDetails) authenticate.getPrincipal();
        return getToken(userDetails);
    }

    @Override
    public Map<String, String> registerUser(RegistrationRequestDto registrationRequestDto) {
        // Überprüfen, ob der Benutzer bereits existiert
        Optional<User> existingUser = userRepository.findByUsername(registrationRequestDto.username());
        if (existingUser.isPresent()) {
            throw new RuntimeException("User already exists");
        }

        // Erstellen und Speichern des neuen Benutzers
        User newUser = new User(
                registrationRequestDto.username(),
                passwordEncoder.encode(registrationRequestDto.password()),
                registrationRequestDto.firstname(),
                registrationRequestDto.lastname(),
                registrationRequestDto.role(),
                new User.Address(registrationRequestDto.street(), registrationRequestDto.city())
        );
        userRepository.save(newUser);
        return Map.of("message", "User registered successfully");
    }


    public Map<String, String> getToken(UserDetails userDetails) {
        final var roles = userDetails.getAuthorities();
        final var username = userDetails.getUsername();
        final var token = jwtService.generateToken(Map.of("role", roles), username);
        return Map.of("token", token);
    }
}