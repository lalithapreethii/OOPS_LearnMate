package com.knowwhereyoulack.service.impl;

import org.springframework.stereotype.Service;

import com.knowwhereyoulack.dto.WeaknessAnalysisResponse;
import com.knowwhereyoulack.service.AnalysisService;
import com.knowwhereyoulack.service.MLPredictionService;

@Service
public class AnalysisServiceImpl implements AnalysisService {

    private final MLPredictionService mlService;

    public AnalysisServiceImpl(MLPredictionService mlService) {
        this.mlService = mlService;
    }

    @Override
    public WeaknessAnalysisResponse analyzeUser(Long userId) {
        return mlService.predictWeakness(userId);
    }
}