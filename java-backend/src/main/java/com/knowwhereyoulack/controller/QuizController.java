package com.knowwhereyoulack.controller;

import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.knowwhereyoulack.dto.QuizSubmissionRequest;
import com.knowwhereyoulack.model.QuizAttempt;
import com.knowwhereyoulack.model.Topic;
import com.knowwhereyoulack.repository.QuizAttemptRepository;
import com.knowwhereyoulack.service.QuizService;

@RestController
@RequestMapping("/api/quiz")
public class QuizController {

    private final QuizService quizService;
    private final QuizAttemptRepository quizAttemptRepository;

    public QuizController(QuizService quizService, QuizAttemptRepository quizAttemptRepository) {
        this.quizService = quizService;
        this.quizAttemptRepository = quizAttemptRepository;
    }

    @GetMapping("/topics")
    public ResponseEntity<List<Topic>> topics() {
        return ResponseEntity.ok(quizService.getAllTopics());
    }

    @GetMapping("/{topicId}")
    @PreAuthorize("hasAnyRole('STUDENT','ADMIN','TEACHER')")
    public ResponseEntity<?> generateQuiz(@PathVariable Long topicId, @RequestParam(required = false) Long userId) {
        var quiz = quizService.generateQuiz(topicId, userId);
        return ResponseEntity.ok(quiz);
    }

    @PostMapping("/submit")
    @PreAuthorize("hasRole('STUDENT')")
    public ResponseEntity<?> submitQuiz(@RequestBody QuizSubmissionRequest req) {
        String result = quizService.submitQuiz(req);
        return ResponseEntity.ok(Map.of("message", result));
    }

    @GetMapping("/history/{userId}")
    @PreAuthorize("hasAnyRole('STUDENT','ADMIN','TEACHER')")
    public ResponseEntity<?> history(@PathVariable Long userId) {
        List<QuizAttempt> attempts = quizAttemptRepository.findByUser_UserId(userId);
        return ResponseEntity.ok(attempts);
    }
}