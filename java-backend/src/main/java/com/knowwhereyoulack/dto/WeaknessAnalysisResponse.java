package com.knowwhereyoulack.dto;

public class WeaknessAnalysisResponse {
    private String topicName;
    private String weaknessLevel;
    private Double accuracyPercentage;

    // Getters and Setters
    public String getTopicName() {
        return topicName;
    }

    public void setTopicName(String topicName) {
        this.topicName = topicName;
    }

    public String getWeaknessLevel() {
        return weaknessLevel;
    }

    public void setWeaknessLevel(String weaknessLevel) {
        this.weaknessLevel = weaknessLevel;
    }

    public Double getAccuracyPercentage() {
        return accuracyPercentage;
    }

    public void setAccuracyPercentage(Double accuracyPercentage) {
        this.accuracyPercentage = accuracyPercentage;
    }
}