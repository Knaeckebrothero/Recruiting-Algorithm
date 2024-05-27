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

    private String name;  // Wird als "username" verwendet
    private String password;
    private String firstname;
    private String lastname;
    private String role;  // Rollen als einfache Zeichenkette

    @Embedded
    private Address address;

    // Angepasster Konstruktor, der den Parametern entspricht, die für die Registrierung verwendet werden
    public User(String username, String password, String firstname, String lastname, String role, Address address) {
        this.name = username;
        this.password = password;
        this.firstname = firstname;
        this.lastname = lastname;
        this.role = role;
        this.address = address;
    }

    @Embeddable
    @Data
    public static class Address {
        private String street;
        private String city;
        @Column(name = "addr_index")
        private int index;

        // Konstruktor für die Adressklasse
        public Address(String street, String city) {
            this.street = street;
            this.city = city;
        }

        // No-args Konstruktor für JPA
        public Address() {}
    }
}