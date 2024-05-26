package fra.uas.intellimatch.intellimatch.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;


@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SurveySections {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private int order;
    private String title;
    private String description;

    @ManyToOne
    @JoinColumn(name = "survey_id")
    private Survey survey;
}
