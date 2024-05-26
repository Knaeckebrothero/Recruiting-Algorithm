package fra.uas.intellimatch.intellimatch.auth;

import fra.uas.intellimatch.intellimatch.auth.dto.AuthRequestDto;
import fra.uas.intellimatch.intellimatch.auth.dto.RegistrationRequestDto;
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
import org.springframework.stereotype.Service;

import java.security.Key;
import java.util.Collections;
import java.util.Date;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthServiceImpl {
    private final AuthenticationManager authenticationManager;
    private final JwtUtility jwtUtility;

    public Map<String, String> authRequest(AuthRequestDto authRequestDto) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(authRequestDto.username(), authRequestDto.password())
        );
        UserDetails userDetails = (UserDetails) authentication.getPrincipal();
        String token = jwtUtility.generateToken(Map.of("role", userDetails.getAuthorities()), userDetails.getUsername());
        return Map.of("token", token);
    }

    public Map<String, String> registerUser(RegistrationRequestDto registrationRequestDto) {
        // Logik zur Benutzerregistrierung hier implementieren, falls notwendig
        return Map.of(); // Rückgabe einer leeren Map oder einer Erfolgsmeldung
    }
}