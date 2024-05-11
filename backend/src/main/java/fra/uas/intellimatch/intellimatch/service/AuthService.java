package fra.uas.intellimatch.intellimatch.service;

import fra.uas.intellimatch.intellimatch.dto.AuthRequestDto;

import java.util.Map;

public interface AuthService {
     Map<String, String> authRequest(AuthRequestDto authRequestDto);

}
