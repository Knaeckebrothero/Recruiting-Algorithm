package fra.uas.intellimatch.intellimatch.model;

import jakarta.persistence.*;
import java.util.List;

@Entity
public class Survey {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @OneToMany(mappedBy = "surveyId")
    private List<SurveySection> sections;

    // Getters and Setters
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public List<SurveySection> getSections() {
        return sections;
    }

    public void setSections(List<SurveySection> sections) {
        this.sections = sections;
    }
}

