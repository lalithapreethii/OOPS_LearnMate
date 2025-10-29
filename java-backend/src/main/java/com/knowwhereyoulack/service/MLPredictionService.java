package com.knowwhereyoulack.service;

import com.knowwhereyoulack.dto.WeaknessAnalysisResponse;

public interface MLPredictionService {
    WeaknessAnalysisResponse predictWeakness(Long userId);
}