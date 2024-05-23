package com.example.intellimatch.repository;

import com.example.intellimatch.model.SurveySection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SurveySectionRepository extends JpaRepository<SurveySection, Integer> {

}

