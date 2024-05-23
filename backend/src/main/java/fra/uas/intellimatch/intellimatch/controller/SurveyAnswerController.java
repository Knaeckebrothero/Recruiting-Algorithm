package fra.uas.intellimatch.intellimatch.controller;

import fra.uas.intellimatch.intellimatch.model.SurveyAnswer;
import fra.uas.intellimatch.intellimatch.service.SurveyAnswerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/survey-answers")
public class SurveyAnswerController {

    private final SurveyAnswerService surveyAnswerService;

    @Autowired
    public SurveyAnswerController(SurveyAnswerService surveyAnswerService) {
        this.surveyAnswerService = surveyAnswerService;
    }

    @GetMapping
    public ResponseEntity<List<SurveyAnswer>> getAllSurveyAnswers() {
        List<SurveyAnswer> surveyAnswers = surveyAnswerService.getAllSurveyAnswers();
        return ResponseEntity.ok(surveyAnswers);
    }

    @GetMapping("/{answerId}")
    public ResponseEntity<SurveyAnswer> getSurveyAnswerById(@PathVariable String answerId) {
        Optional<SurveyAnswer> surveyAnswer = surveyAnswerService.getSurveyAnswerById(answerId);
        return surveyAnswer.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<SurveyAnswer> createSurveyAnswer(@RequestBody SurveyAnswer surveyAnswer) {
        surveyAnswerService.saveSurveyAnswer(surveyAnswer);
        return new ResponseEntity<>(surveyAnswer, HttpStatus.CREATED);
    }

    @PutMapping("/{answerId}")
    public ResponseEntity<SurveyAnswer> updateSurveyAnswer(@PathVariable String answerId, @RequestBody SurveyAnswer updatedAnswer) {
        Optional<SurveyAnswer> existingAnswer = surveyAnswerService.getSurveyAnswerById(answerId);
        if (existingAnswer.isPresent()) {
            SurveyAnswer existingAnswerEntity = existingAnswer.get();
            existingAnswerEntity.setId(Integer.parseInt(answerId));
            existingAnswerEntity.setResponse(updatedAnswer.getResponse());
            surveyAnswerService.saveSurveyAnswer(existingAnswerEntity);
            return ResponseEntity.ok(existingAnswerEntity);
        } else {
            return ResponseEntity.notFound().build();
        }
    }


    @DeleteMapping("/{answerId}")
    public ResponseEntity<Void> deleteSurveyAnswer(@PathVariable String answerId) {
        Optional<SurveyAnswer> surveyAnswer = surveyAnswerService.getSurveyAnswerById(answerId);
        if (surveyAnswer.isPresent()) {
            surveyAnswerService.deleteSurveyAnswer(answerId);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}

