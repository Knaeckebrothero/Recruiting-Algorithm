package fra.uas.intellimatch.intellimatch.auth;

import fra.uas.intellimatch.intellimatch.model.User;
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
        User.Address userAddress = new User.Address("1234 Address Street", "Anytown");
        User.Address businessUserAddress = new User.Address("4321 Business Ave", "Businesstown");

        users.put(USER, new User(
                USER,
                "{noop}" + USER,
                USER_ROLE,
                "User",       // First name
                "Example",    // Last name
                userAddress
        ));
        users.put(BUSINESSUSER, new User(
                BUSINESSUSER,
                "{noop}" + BUSINESSUSER,
                BUSINESSUSER_ROLE,
                "Business",   // First name
                "User",       // Last name
                businessUserAddress
        ));
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return Optional.ofNullable(users.get(username))
                .map(this::getUser)
                .orElseThrow(() -> new UsernameNotFoundException("User not found: " + username));
    }

    private UserDetails getUser(User user) {
        return org.springframework.security.core.userdetails.User
                .withUsername(user.getName())
                .password(user.getPassword())
                .roles(user.getRole())
                .build();
    }

    public void saveUser(User user) {
        if (users.containsKey(user.getName())) {
            throw new RuntimeException("User already exists");
        }
        users.put(user.getName(), user);
    }
}