package fra.uas.intellimatch.intellimatch.user;

import java.util.List;

public record User(
        String username,
        String password,
        List<String> roles,
        String firstname,
        String lastname,
        String address
) {}