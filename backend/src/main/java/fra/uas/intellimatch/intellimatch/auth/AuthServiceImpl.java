package fra.uas.intellimatch.intellimatch.auth;

import fra.uas.intellimatch.intellimatch.auth.dto.AuthRequestDto;
import fra.uas.intellimatch.intellimatch.auth.dto.RegistrationRequestDto;
import fra.uas.intellimatch.intellimatch.model.User;
import fra.uas.intellimatch.intellimatch.repository.UserRepository;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.security.Key;
import java.util.Collections;
import java.util.Date;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthServiceImpl implements AuthService {
    private final AuthenticationManager authenticationManager;
    private final JwtUtility jwtUtility;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public Map<String, String> authRequest(AuthRequestDto authRequestDto) {
        return Map.of();
    }

    @Override
    public Map<String, String> registerUser(RegistrationRequestDto registrationRequestDto) {
        userRepository.findByUsername(registrationRequestDto.username()).ifPresent(user -> {
            throw new IllegalArgumentException ("Username already exists: " + registrationRequestDto.username());
        });

        User newUser = new User(
                registrationRequestDto.username(),
                passwordEncoder.encode(registrationRequestDto.password()),
                registrationRequestDto.firstname(),
                registrationRequestDto.lastname(),
                registrationRequestDto.street(),
                registrationRequestDto.city(),
                Collections.singletonList(registrationRequestDto.role())
        );

        userRepository.save(newUser);

        // Generierung des JWT für den neu registrierten Benutzer
        String token = jwtUtility.generateToken(Map.of("role", newUser.getRole()), newUser.getName());

        log.info("User registered successfully: {}", registrationRequestDto.username());

        return Map.of(
                "message", "User registered successfully",
                "token", token
        );
    }
}