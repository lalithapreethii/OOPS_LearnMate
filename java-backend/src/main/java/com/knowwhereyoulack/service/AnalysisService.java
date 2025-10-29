package com.knowwhereyoulack.service;

import com.knowwhereyoulack.dto.WeaknessAnalysisResponse;

public interface AnalysisService {
    WeaknessAnalysisResponse analyzeUser(Long userId);
}