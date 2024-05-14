package fra.uas.intellimatch.intellimatch.controller;

import fra.uas.intellimatch.intellimatch.dto.AuthRequestDto;
import fra.uas.intellimatch.intellimatch.dto.RegistrationRequestDto;
import fra.uas.intellimatch.intellimatch.service.AuthService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/auth/v1")
@Slf4j
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;
    @PostMapping("/login")
    public ResponseEntity<Map<String, String>> authRequest(@RequestBody AuthRequestDto authRequestDto) {
        log.info("AuthResource.authRequest start {}", authRequestDto);
        var userRegistrationResponse = authService.authRequest(authRequestDto);
        log.info("AuthResource.authRequest end {}", userRegistrationResponse);
        return new ResponseEntity<>(userRegistrationResponse, HttpStatus.OK);
    }
    @PostMapping("/register")
    public ResponseEntity<Map<String, String>> registerUser(@RequestBody RegistrationRequestDto registrationRequestDto) {
        log.info("Registration attempt for username: {}", registrationRequestDto.username());
        var registrationResponse = authService.registerUser(registrationRequestDto);
        log.info("Registration completed for username: {}", registrationRequestDto.username());
        return new ResponseEntity<>(registrationResponse, HttpStatus.CREATED);
    }
}
