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
    private String firstname;
    private String lastname;

    private String role;  // Rollen als einfache Zeichenkette

    @Embedded
    private Address address;

    public User(String username, String encode, String firstname, String lastname, String street, String city, List<String> strings) {
    }


    @Embeddable
    @Data
    public static class Address {
        private String street;
        private String city;
        @Column(name = "addr_index")
        private int index;
    }
}
