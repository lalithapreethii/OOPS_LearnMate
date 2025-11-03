package com.knowwhereyoulack.controller;

import com.knowwhereyoulack.model.WeakTopic;
import com.knowwhereyoulack.service.AnalyticsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/analytics")
@CrossOrigin(origins = "http://localhost:5173")
public class AnalyticsController {
    
    @Autowired
    private AnalyticsService analyticsService;
    
    // Get weak topics
    @GetMapping("/weak-topics/{userId}")
    public ResponseEntity<List<WeakTopic>> getWeakTopics(@PathVariable Long userId) {
        return ResponseEntity.ok(analyticsService.getWeakTopics(userId));
    }
    
    // Get overall progress
    @GetMapping("/progress/{userId}")
    public ResponseEntity<Map<String, Object>> getOverallProgress(@PathVariable Long userId) {
        Map<String, Object> progress = new HashMap<>();
        progress.put("averageAccuracy", analyticsService.getAverageAccuracy(userId));
        progress.put("totalQuizzes", analyticsService.getTotalQuizzes(userId));
        progress.put("weeklyStreak", analyticsService.getWeeklyStreak(userId));
        return ResponseEntity.ok(progress);
    }
    
    // Get dashboard stats
    @GetMapping("/dashboard/{userId}")
    public ResponseEntity<Map<String, Object>> getDashboardStats(@PathVariable Long userId) {
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalQuizzes", analyticsService.getTotalQuizzes(userId));
        stats.put("averageScore", analyticsService.getAverageAccuracy(userId));
        stats.put("weeklyStreak", analyticsService.getWeeklyStreak(userId));
        stats.put("weakTopics", analyticsService.getWeakTopics(userId));
        stats.put("recentAccuracy", analyticsService.getRecentQuizAccuracy(userId));
        return ResponseEntity.ok(stats);
    }
    
    // Save quiz result
    @PostMapping("/quiz-result")
    public ResponseEntity<Map<String, String>> saveQuizResult(@RequestBody Map<String, Object> quizResult) {
        try {
            analyticsService.saveQuizResult(quizResult);
            return ResponseEntity.ok(Map.of(
                "status", "success",
                "message", "Quiz result saved successfully"
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "status", "error",
                "message", "Failed to save quiz result: " + e.getMessage()
            ));
        }
    }
}
