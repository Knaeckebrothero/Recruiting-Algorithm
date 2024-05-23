package com.example.intellimatch.controller;

import com.example.intellimatch.model.SurveyQuestion;
import com.example.intellimatch.service.SurveyQuestionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/survey-questions")
public class SurveyQuestionController {

    private final SurveyQuestionService surveyQuestionService;

    @Autowired
    public SurveyQuestionController(SurveyQuestionService surveyQuestionService) {
        this.surveyQuestionService = surveyQuestionService;
    }

    @GetMapping
    public ResponseEntity<List<SurveyQuestion>> getAllSurveyQuestions() {
        List<SurveyQuestion> surveyQuestions = surveyQuestionService.getAllSurveyQuestions();
        return ResponseEntity.ok(surveyQuestions);
    }

    @GetMapping("/{questionId}")
    public ResponseEntity<SurveyQuestion> getSurveyQuestionById(@PathVariable Integer questionId) {
        Optional<SurveyQuestion> surveyQuestion = surveyQuestionService.getSurveyQuestionById(questionId);
        return surveyQuestion.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<SurveyQuestion> createSurveyQuestion(@RequestBody SurveyQuestion surveyQuestion) {
        surveyQuestionService.saveSurveyQuestion(surveyQuestion);
        return new ResponseEntity<>(surveyQuestion, HttpStatus.CREATED);
    }

    @PutMapping("/{questionId}")
    public ResponseEntity<SurveyQuestion> updateSurveyQuestion(@PathVariable Integer questionId, @RequestBody SurveyQuestion updatedQuestion) {
        Optional<SurveyQuestion> existingQuestion = surveyQuestionService.getSurveyQuestionById(questionId);
        if (existingQuestion.isPresent()) {
            updatedQuestion.setId(questionId);
            surveyQuestionService.saveSurveyQuestion(updatedQuestion);
            return ResponseEntity.ok(updatedQuestion);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{questionId}")
    public ResponseEntity<Void> deleteSurveyQuestion(@PathVariable Integer questionId) {
        Optional<SurveyQuestion> surveyQuestion = surveyQuestionService.getSurveyQuestionById(questionId);
        if (surveyQuestion.isPresent()) {
            surveyQuestionService.deleteSurveyQuestion(questionId);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}

