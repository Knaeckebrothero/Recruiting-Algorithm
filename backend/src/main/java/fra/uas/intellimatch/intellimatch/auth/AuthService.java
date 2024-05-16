package fra.uas.intellimatch.intellimatch.auth;

import fra.uas.intellimatch.intellimatch.dto.RegistrationRequestDto;

import java.util.Map;

public interface AuthService {
     Map<String, String> authRequest(AuthRequestDto authRequestDto);
     Map<String, String> registerUser(RegistrationRequestDto registrationRequestDto);
}
