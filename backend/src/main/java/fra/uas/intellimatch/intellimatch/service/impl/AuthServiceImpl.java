package fra.uas.intellimatch.intellimatch.service.impl;

import fra.uas.intellimatch.intellimatch.dto.AuthRequestDto;
import fra.uas.intellimatch.intellimatch.dto.RegistrationRequestDto;
import fra.uas.intellimatch.intellimatch.dto.User;
import fra.uas.intellimatch.intellimatch.security.InMemoryUserDetailsService;
import fra.uas.intellimatch.intellimatch.service.AuthService;
import fra.uas.intellimatch.intellimatch.service.JwtService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthServiceImpl implements AuthService {
    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;
    private final InMemoryUserDetailsService userDetailsService;

    @Override
    public Map<String, String> authRequest(AuthRequestDto authRequestDto) {
       final var authenticate = authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(authRequestDto.userName(), authRequestDto.password()));
       final var userDetails =  (UserDetails) authenticate.getPrincipal();
       return   getToken(userDetails);
    }
    @Override
    public Map<String, String> registerUser(RegistrationRequestDto registrationRequestDto) {
        userDetailsService.saveUser(new User(registrationRequestDto.username(), "{noop}" + registrationRequestDto.password(), List.of("USER")));
        return Map.of("message", "User registered successfully");
    }
    public Map<String, String> getToken( UserDetails userDetails) {
        final var roles = userDetails.getAuthorities();
        final var username = userDetails.getUsername();
        final var token = jwtService.generateToken(Map.of("role", roles), username);
        return Map.of("token", token);
    }
}
