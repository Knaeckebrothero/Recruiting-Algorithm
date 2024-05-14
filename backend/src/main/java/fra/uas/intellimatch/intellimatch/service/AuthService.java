package fra.uas.intellimatch.intellimatch.service;

import fra.uas.intellimatch.intellimatch.dto.AuthRequestDto;
import fra.uas.intellimatch.intellimatch.dto.RegistrationRequestDto;

import java.util.Map;

public interface AuthService {
     Map<String, String> authRequest(AuthRequestDto authRequestDto);
     Map<String, String> registerUser(RegistrationRequestDto registrationRequestDto);

}
