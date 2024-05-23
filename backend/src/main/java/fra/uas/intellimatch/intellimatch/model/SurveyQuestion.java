package fra.uas.intellimatch.intellimatch.model;

import jakarta.persistence.*;
import java.util.List;

@Entity
public class SurveyQuestion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private Integer sectionId;
    private String question;

    @ManyToOne
    @JoinColumn(name = "section_id", insertable = false, updatable = false)
    private SurveySection surveySection;

    @OneToMany(mappedBy = "questionId")
    private List<SurveyAnswer> surveyAnswers;

    // Getters and Setters
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getSectionId() {
        return sectionId;
    }

    public void setSectionId(Integer sectionId) {
        this.sectionId = sectionId;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public SurveySection getSurveySection() {
        return surveySection;
    }

    public void setSurveySection(SurveySection surveySection) {
        this.surveySection = surveySection;
    }

    public List<SurveyAnswer> getSurveyAnswers() {
        return surveyAnswers;
    }

    public void setSurveyAnswers(List<SurveyAnswer> surveyAnswers) {
        this.surveyAnswers = surveyAnswers;
    }
}
