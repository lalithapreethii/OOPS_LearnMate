package com.knowwhereyoulack.model;

public class WeakTopic {
    private String topic;
    private Double currentScore;
    private Double goalScore;
    private Integer totalAttempts;
    
    public WeakTopic(String topic, Double currentScore, Integer totalAttempts) {
        this.topic = topic;
        this.currentScore = currentScore;
        this.totalAttempts = totalAttempts;
        this.goalScore = 80.0; // Default goal
    }
    
    // Getters and Setters
    public String getTopic() { return topic; }
    public void setTopic(String topic) { this.topic = topic; }
    
    public Double getCurrentScore() { return currentScore; }
    public void setCurrentScore(Double currentScore) { this.currentScore = currentScore; }
    
    public Double getGoalScore() { return goalScore; }
    public void setGoalScore(Double goalScore) { this.goalScore = goalScore; }
    
    public Integer getTotalAttempts() { return totalAttempts; }
    public void setTotalAttempts(Integer totalAttempts) { this.totalAttempts = totalAttempts; }
}
