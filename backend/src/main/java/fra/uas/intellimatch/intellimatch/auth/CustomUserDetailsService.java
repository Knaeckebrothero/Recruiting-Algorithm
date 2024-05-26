package fra.uas.intellimatch.intellimatch.auth;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.security.core.userdetails.User;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // Hier würden Sie Ihre Datenbankabfrage durchführen, um den Benutzer zu finden
        // Beispiel mit festem Benutzer:
        return User.withUsername("user")
                .password("{noop}password")
                .roles("USER")
                .build();
    }
}
