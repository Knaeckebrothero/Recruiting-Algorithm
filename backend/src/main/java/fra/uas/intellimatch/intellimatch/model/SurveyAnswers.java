package fra.uas.intellimatch.intellimatch.model;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SurveyAnswers {
    @Id
    private String id;

    private int response;

    @ManyToOne
    @JoinColumn(name = "question_id")
    private SurveyQuestions question;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
}

