package fra.uas.intellimatch.intellimatch.model;
import jakarta.persistence.*;
import lombok.*;
import java.util.List;

@Entity
@Data
@NoArgsConstructor
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private String name;
    private String password;
    @ElementCollection(fetch = FetchType.EAGER)
    private List<String> roles;
    private String firstname;
    private String lastname;

    @Embedded
    private Address address;

    @Enumerated(EnumType.STRING)
    private UserRoles role;

    @Embeddable
    @Data
    public static class Address {
        private String street;
        private String city;
        @Column(name = "addr_index")
        private int index;
    }
}