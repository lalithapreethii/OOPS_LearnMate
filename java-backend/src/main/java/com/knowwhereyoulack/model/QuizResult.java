package com.knowwhereyoulack.model;

import jakarta.persistence.*;
import java.util.Date;

@Entity
@Table(name = "quiz_results")
public class QuizResult {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private Long userId;
    private Long quizId;
    private String topic;
    private Integer score;
    private Integer totalQuestions;
    private Double accuracy;
    
    @Temporal(TemporalType.TIMESTAMP)
    private Date completedAt;
    
    @PrePersist
    protected void onCreate() {
        completedAt = new Date();
        if (totalQuestions > 0) {
            accuracy = (score.doubleValue() / totalQuestions) * 100;
        }
    }
    
    // Constructors
    public QuizResult() {}
    
    public QuizResult(Long userId, Long quizId, String topic, Integer score, Integer totalQuestions) {
        this.userId = userId;
        this.quizId = quizId;
        this.topic = topic;
        this.score = score;
        this.totalQuestions = totalQuestions;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
    
    public Long getQuizId() { return quizId; }
    public void setQuizId(Long quizId) { this.quizId = quizId; }
    
    public String getTopic() { return topic; }
    public void setTopic(String topic) { this.topic = topic; }
    
    public Integer getScore() { return score; }
    public void setScore(Integer score) { this.score = score; }
    
    public Integer getTotalQuestions() { return totalQuestions; }
    public void setTotalQuestions(Integer totalQuestions) { this.totalQuestions = totalQuestions; }
    
    public Double getAccuracy() { return accuracy; }
    public void setAccuracy(Double accuracy) { this.accuracy = accuracy; }
    
    public Date getCompletedAt() { return completedAt; }
    public void setCompletedAt(Date completedAt) { this.completedAt = completedAt; }
}
