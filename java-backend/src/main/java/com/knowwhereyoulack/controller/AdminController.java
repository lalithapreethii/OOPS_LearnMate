package com.knowwhereyoulack.controller;

import com.knowwhereyoulack.model.*;
import com.knowwhereyoulack.repository.*;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Minimal admin endpoints for content management.
 */
@RestController
@RequestMapping("/api/admin")
@PreAuthorize("hasAnyRole('ADMIN','TEACHER')")
public class AdminController {

    private final SubjectRepository subjectRepository;
    private final TopicRepository topicRepository;
    private final QuestionRepository questionRepository;
    private final LearningResourceRepository learningResourceRepository;

    public AdminController(SubjectRepository subjectRepository,
                           TopicRepository topicRepository,
                           QuestionRepository questionRepository,
                           LearningResourceRepository learningResourceRepository) {
        this.subjectRepository = subjectRepository;
        this.topicRepository = topicRepository;
        this.questionRepository = questionRepository;
        this.learningResourceRepository = learningResourceRepository;
    }

    @PostMapping("/subject")
    public ResponseEntity<?> createSubject(@RequestBody Subject subject) {
        Subject s = subjectRepository.save(subject);
        return ResponseEntity.ok(s);
    }

    @PostMapping("/topic")
    public ResponseEntity<?> createTopic(@RequestBody Topic topic) {
        Topic t = topicRepository.save(topic);
        return ResponseEntity.ok(t);
    }

    @PostMapping("/question")
    public ResponseEntity<?> createQuestion(@RequestBody Question question) {
        Question q = questionRepository.save(question);
        return ResponseEntity.ok(q);
    }

    @PostMapping("/resource")
    public ResponseEntity<?> addResource(@RequestBody LearningResource resource) {
        LearningResource r = learningResourceRepository.save(resource);
        return ResponseEntity.ok(r);
    }

    @GetMapping("/subjects")
    public ResponseEntity<List<Subject>> listSubjects() {
        return ResponseEntity.ok(subjectRepository.findAll());
    }
}