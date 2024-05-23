package com.example.intellimatch.controller;

import com.example.intellimatch.model.Survey;
import com.example.intellimatch.service.SurveyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/surveys")
public class SurveyController {

    private final SurveyService surveyService;

    @Autowired
    public SurveyController(SurveyService surveyService) {
        this.surveyService = surveyService;
    }

    @GetMapping
    public ResponseEntity<List<Survey>> getAllSurveys() {
        List<Survey> surveys = surveyService.getAllSurveys();
        return ResponseEntity.ok(surveys);
    }

    @GetMapping("/{surveyId}")
    public ResponseEntity<Survey> getSurveyById(@PathVariable Integer surveyId) {
        Optional<Survey> survey = surveyService.getSurveyById(surveyId);
        return survey.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Survey> createSurvey(@RequestBody Survey survey) {
        surveyService.saveSurvey(survey);
        return new ResponseEntity<>(survey, HttpStatus.CREATED);
    }

    @PutMapping("/{surveyId}")
    public ResponseEntity<Survey> updateSurvey(@PathVariable Integer surveyId, @RequestBody Survey updatedSurvey) {
        Optional<Survey> existingSurvey = surveyService.getSurveyById(surveyId);
        if (existingSurvey.isPresent()) {
            updatedSurvey.setId(surveyId);
            surveyService.saveSurvey(updatedSurvey);
            return ResponseEntity.ok(updatedSurvey);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{surveyId}")
    public ResponseEntity<Void> deleteSurvey(@PathVariable Integer surveyId) {
        Optional<Survey> survey = surveyService.getSurveyById(surveyId);
        if (survey.isPresent()) {
            surveyService.deleteSurvey(surveyId);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}

