package fra.uas.intellimatch.intellimatch.security;

import fra.uas.intellimatch.intellimatch.user.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class InMemoryUserDetailsService implements UserDetailsService {
    public static final String USER = "user";
    public static final String BUSINESSUSER = "businessuser";
    public static final String USER_ROLE = "USER";
    public static final String BUSINESSUSER_ROLE = "BUSINESSUSER";

    private final Map<String, User> users = new ConcurrentHashMap<>();

    public InMemoryUserDetailsService() {
        users.put(USER, new User(
                USER,
                "{noop}" + USER,
                List.of(USER_ROLE),
                "User",       // Beispiel-Vorname
                "Example",    // Beispiel-Nachname
                "1234 Address Street"  // Beispiel-Adresse
        ));
        users.put(BUSINESSUSER, new User(
                BUSINESSUSER,
                "{noop}" + BUSINESSUSER,
                List.of(BUSINESSUSER_ROLE),
                "Business",   // Beispiel-Vorname
                "User",       // Beispiel-Nachname
                "4321 Business Ave"    // Beispiel-Adresse
        ));
    }
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return Optional.ofNullable(users.get(username))
                .map(this::getUser)
                .orElseThrow(() -> new RuntimeException(String.format("user = %s not present", username)));
    }
    private UserDetails getUser(User user) {
        return org.springframework.security.core.userdetails.User
                .withUsername(user.username())
                .password(user.password())
                .roles(user.roles().toArray(new String[0]))
                .build();
    }
    public void saveUser(User user) {
        if (users.containsKey(user.username())) {
            throw new RuntimeException("User already exists");
        }
        users.put(user.username(), user);
    }
}

