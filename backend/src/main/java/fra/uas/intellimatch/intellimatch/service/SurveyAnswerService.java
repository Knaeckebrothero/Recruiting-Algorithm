package fra.uas.intellimatch.intellimatch.service;

import fra.uas.intellimatch.intellimatch.model.SurveyAnswer;
import fra.uas.intellimatch.intellimatch.repository.SurveyAnswerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class SurveyAnswerService {

    private final SurveyAnswerRepository surveyAnswerRepository;

    @Autowired
    public SurveyAnswerService(SurveyAnswerRepository surveyAnswerRepository) {
        this.surveyAnswerRepository = surveyAnswerRepository;
    }

    public List<SurveyAnswer> getAllSurveyAnswers() {
        return surveyAnswerRepository.findAll();
    }

    public Optional<SurveyAnswer> getSurveyAnswerById(String answerId) {
        return surveyAnswerRepository.findById(answerId);
    }

    public void saveSurveyAnswer(SurveyAnswer surveyAnswer) {
        surveyAnswerRepository.save(surveyAnswer);
    }

    public void deleteSurveyAnswer(String answerId) {
        surveyAnswerRepository.deleteById(answerId);
    }
}
