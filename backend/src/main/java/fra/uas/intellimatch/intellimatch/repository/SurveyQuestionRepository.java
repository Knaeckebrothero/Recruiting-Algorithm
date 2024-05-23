package fra.uas.intellimatch.intellimatch.repository;

import fra.uas.intellimatch.intellimatch.model.SurveyQuestion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SurveyQuestionRepository extends JpaRepository<SurveyQuestion, Integer> {

}

