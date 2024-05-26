package fra.uas.intellimatch.intellimatch.service;

import fra.uas.intellimatch.intellimatch.model.Survey;
import fra.uas.intellimatch.intellimatch.repository.SurveyRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class SurveyService {

    @Autowired
    private SurveyRepository surveyRepository;

    public List<Survey> findAllSurveys() {
        return surveyRepository.findAll();
    }

    public Optional<Survey> findSurveyById(int id) {
        return surveyRepository.findById(id);
    }

    public Survey saveSurvey(Survey survey) {
        return surveyRepository.save(survey);
    }
}
