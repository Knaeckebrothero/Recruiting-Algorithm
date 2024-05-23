package fra.uas.intellimatch.intellimatch.repository;

import fra.uas.intellimatch.intellimatch.model.SurveySection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SurveySectionRepository extends JpaRepository<SurveySection, Integer> {

}

