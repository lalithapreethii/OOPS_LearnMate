package com.knowwhereyoulack.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.knowwhereyoulack.dto.WeaknessAnalysisResponse;
import com.knowwhereyoulack.service.AnalysisService;

@RestController
@RequestMapping("/api/analysis")
public class AnalysisController {

    private final AnalysisService analysisService;

    public AnalysisController(AnalysisService analysisService) {
        this.analysisService = analysisService;
    }

    @GetMapping("/{userId}")
    @PreAuthorize("hasAnyRole('STUDENT','ADMIN','TEACHER')")
    public ResponseEntity<WeaknessAnalysisResponse> getAnalysis(@PathVariable Long userId) {
        return ResponseEntity.ok(analysisService.analyzeUser(userId));
    }

    @PostMapping("/refresh")
    @PreAuthorize("hasAnyRole('ADMIN','TEACHER')")
    public ResponseEntity<?> refreshAnalysis(@RequestParam Long userId) {
        // In production: enqueue job / call ML microservice to recompute and persist analyses
        WeaknessAnalysisResponse res = analysisService.analyzeUser(userId);
        return ResponseEntity.ok(res);
    }
}