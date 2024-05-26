package fra.uas.intellimatch.intellimatch.model;

import jakarta.persistence.*;
import lombok.*;

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

    @Embeddable
    @Data
    public static class Address {
        private String street;
        private String city;
        @Column(name = "addr_index")
        private int index;
    }
}
