package com.example.intellimatch.service;

import com.example.intellimatch.model.Survey;
import com.example.intellimatch.repository.SurveyRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class SurveyService {

    private final SurveyRepository surveyRepository;

    @Autowired
    public SurveyService(SurveyRepository surveyRepository) {
        this.surveyRepository = surveyRepository;
    }

    public List<Survey> getAllSurveys() {
        return surveyRepository.findAll();
    }

    public Optional<Survey> getSurveyById(Integer surveyId) {
        return surveyRepository.findById(surveyId);
    }

    public void saveSurvey(Survey survey) {
        surveyRepository.save(survey);
    }

    public void deleteSurvey(Integer surveyId) {
        surveyRepository.deleteById(surveyId);
    }
}

