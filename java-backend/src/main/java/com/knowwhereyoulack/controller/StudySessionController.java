package com.knowwhereyoulack.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * Study Session Controller
 * Handles timer/study session tracking
 */
@RestController
@RequestMapping("/api/study-sessions")
@CrossOrigin(origins = "http://localhost:5173")
public class StudySessionController {
    
    @PostMapping
    public ResponseEntity<Map<String, String>> saveSession(@RequestBody Map<String, Object> session) {
        // Log the session for now (later can save to database)
        System.out.println("📚 Study session saved:");
        System.out.println("  User ID: " + session.get("userId"));
        System.out.println("  Duration: " + session.get("durationMinutes") + " minutes");
        System.out.println("  Topic: " + session.get("topic"));
        System.out.println("  Date: " + session.get("sessionDate"));
        
        return ResponseEntity.ok(Map.of(
            "status", "success", 
            "message", "Study session saved successfully"
        ));
    }
    
    @GetMapping("/user/{userId}")
    public ResponseEntity<Map<String, Object>> getUserSessions(@PathVariable Long userId) {
        // Return empty list for now (can implement database query later)
        return ResponseEntity.ok(Map.of(
            "userId", userId,
            "totalSessions", 0,
            "totalMinutes", 0,
            "sessions", new Object[0]
        ));
    }
}
