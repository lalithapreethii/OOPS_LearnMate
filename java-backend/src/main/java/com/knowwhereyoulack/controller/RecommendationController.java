package com.knowwhereyoulack.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.knowwhereyoulack.model.LearningResource;
import com.knowwhereyoulack.model.Topic;
import com.knowwhereyoulack.repository.LearningResourceRepository;
import com.knowwhereyoulack.repository.TopicRepository;

@RestController
@RequestMapping("/api/recommendations")
public class RecommendationController {

    private final LearningResourceRepository resourceRepo;
    private final TopicRepository topicRepo;

    public RecommendationController(LearningResourceRepository resourceRepo, TopicRepository topicRepo) {
        this.resourceRepo = resourceRepo;
        this.topicRepo = topicRepo;
    }

    @GetMapping("/{userId}")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> recommendForUser(@PathVariable Long userId) {
        // Naive: return top resources for topics marked weak by ML (placeholder)
        // For now return all resources; integrate with WeaknessAnalysis later
        return ResponseEntity.ok(resourceRepo.findAll());
    }

    @GetMapping("/topic/{topicId}")
    @PreAuthorize("hasAnyRole('STUDENT','ADMIN','TEACHER')")
    public ResponseEntity<List<LearningResource>> resourcesForTopic(@PathVariable Long topicId) {
        Topic t = topicRepo.findById(topicId).orElseThrow();
        return ResponseEntity.ok(resourceRepo.findByTopic(t));
    }
}