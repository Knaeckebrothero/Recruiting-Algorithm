package com.example.intellimatch.service;

import com.example.intellimatch.model.SurveyQuestion;
import com.example.intellimatch.repository.SurveyQuestionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class SurveyQuestionService {

    private final SurveyQuestionRepository surveyQuestionRepository;

    @Autowired
    public SurveyQuestionService(SurveyQuestionRepository surveyQuestionRepository) {
        this.surveyQuestionRepository = surveyQuestionRepository;
    }

    public List<SurveyQuestion> getAllSurveyQuestions() {
        return surveyQuestionRepository.findAll();
    }

    public Optional<SurveyQuestion> getSurveyQuestionById(Integer questionId) {
        return surveyQuestionRepository.findById(questionId);
    }

    public void saveSurveyQuestion(SurveyQuestion surveyQuestion) {
        surveyQuestionRepository.save(surveyQuestion);
    }

    public void deleteSurveyQuestion(Integer questionId) {
        surveyQuestionRepository.deleteById(questionId);
    }
}

