package fra.uas.intellimatch.intellimatch.dto;

import java.util.List;

public record User(String username, String password, List<String> roles) {
}