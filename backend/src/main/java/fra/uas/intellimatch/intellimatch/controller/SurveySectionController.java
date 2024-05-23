package fra.uas.intellimatch.intellimatch.controller;

import fra.uas.intellimatch.intellimatch.model.SurveySection;
import fra.uas.intellimatch.intellimatch.service.SurveySectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/survey-sections")
public class SurveySectionController {

    private final SurveySectionService surveySectionService;

    @Autowired
    public SurveySectionController(SurveySectionService surveySectionService) {
        this.surveySectionService = surveySectionService;
    }

    @GetMapping
    public ResponseEntity<List<SurveySection>> getAllSurveySections() {
        List<SurveySection> surveySections = surveySectionService.getAllSurveySections();
        return ResponseEntity.ok(surveySections);
    }

    @GetMapping("/{sectionId}")
    public ResponseEntity<SurveySection> getSurveySectionById(@PathVariable Integer sectionId) {
        Optional<SurveySection> surveySection = surveySectionService.getSurveySectionById(sectionId);
        return surveySection.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<SurveySection> createSurveySection(@RequestBody SurveySection surveySection) {
        surveySectionService.saveSurveySection(surveySection);
        return new ResponseEntity<>(surveySection, HttpStatus.CREATED);
    }

    @PutMapping("/{sectionId}")
    public ResponseEntity<SurveySection> updateSurveySection(@PathVariable Integer sectionId, @RequestBody SurveySection updatedSection) {
        Optional<SurveySection> existingSection = surveySectionService.getSurveySectionById(sectionId);
        if (existingSection.isPresent()) {
            updatedSection.setId(sectionId);
            surveySectionService.saveSurveySection(updatedSection);
            return ResponseEntity.ok(updatedSection);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{sectionId}")
    public ResponseEntity<Void> deleteSurveySection(@PathVariable Integer sectionId) {
        Optional<SurveySection> surveySection = surveySectionService.getSurveySectionById(sectionId);
        if (surveySection.isPresent()) {
            surveySectionService.deleteSurveySection(sectionId);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}

