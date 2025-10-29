package com.knowwhereyoulack.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.Objects;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;

/**
 * WeaknessAnalysis Entity
 * 
 * Represents ML model's analysis of a student's performance on a topic
 * This is where ML predictions are stored
 */
@Entity
@Table(name = "weakness_analysis", 
       uniqueConstraints = @UniqueConstraint(columnNames = {"user_id", "topic_id"}))
public class WeaknessAnalysis {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "analysis_id")
    private Long analysisId;

    @Enumerated(EnumType.STRING)
    @Column(name = "strength_level", nullable = false)
    private StrengthLevel strengthLevel;

    @Column(name = "confidence_score", nullable = false, precision = 6, scale = 4)
    private BigDecimal confidenceScore;

    @Column(name = "avg_score", precision = 6, scale = 2)
    private BigDecimal avgScore;

    @Column(name = "total_attempts")
    private Integer totalAttempts = 0;

    @Column(name = "last_attempt_date")
    private LocalDateTime lastAttemptDate;

    @Column(name = "analyzed_at", nullable = false)
    private LocalDateTime analyzedAt;

    // Many-to-One: Many Analyses belong to One User
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    // Many-to-One: Many Analyses belong to One Topic
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "topic_id", nullable = false)
    private Topic topic;

    @PrePersist
    protected void onCreate() {
        analyzedAt = LocalDateTime.now();
    }

    /**
     * Enum for Strength Levels (ML Predictions)
     */
    public enum StrengthLevel {
        WEAK,
        MODERATE,
        STRONG
    }

    // Constructors
    public WeaknessAnalysis() {
    }

    public WeaknessAnalysis(Long analysisId, StrengthLevel strengthLevel, BigDecimal confidenceScore,
                           BigDecimal avgScore, Integer totalAttempts, LocalDateTime lastAttemptDate,
                           LocalDateTime analyzedAt, User user, Topic topic) {
        this.analysisId = analysisId;
        this.strengthLevel = strengthLevel;
        this.confidenceScore = confidenceScore;
        this.avgScore = avgScore;
        this.totalAttempts = totalAttempts;
        this.lastAttemptDate = lastAttemptDate;
        this.analyzedAt = analyzedAt;
        this.user = user;
        this.topic = topic;
    }

    // Getters and Setters
    public Long getAnalysisId() {
        return analysisId;
    }

    public void setAnalysisId(Long analysisId) {
        this.analysisId = analysisId;
    }

    public StrengthLevel getStrengthLevel() {
        return strengthLevel;
    }

    public void setStrengthLevel(StrengthLevel strengthLevel) {
        this.strengthLevel = strengthLevel;
    }

    public BigDecimal getConfidenceScore() {
        return confidenceScore;
    }

    public void setConfidenceScore(BigDecimal confidenceScore) {
        this.confidenceScore = confidenceScore;
    }

    public BigDecimal getAvgScore() {
        return avgScore;
    }

    public void setAvgScore(BigDecimal avgScore) {
        this.avgScore = avgScore;
    }

    public Integer getTotalAttempts() {
        return totalAttempts;
    }

    public void setTotalAttempts(Integer totalAttempts) {
        this.totalAttempts = totalAttempts;
    }

    public LocalDateTime getLastAttemptDate() {
        return lastAttemptDate;
    }

    public void setLastAttemptDate(LocalDateTime lastAttemptDate) {
        this.lastAttemptDate = lastAttemptDate;
    }

    public LocalDateTime getAnalyzedAt() {
        return analyzedAt;
    }

    public void setAnalyzedAt(LocalDateTime analyzedAt) {
        this.analyzedAt = analyzedAt;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Topic getTopic() {
        return topic;
    }

    public void setTopic(Topic topic) {
        this.topic = topic;
    }

    /**
     * Business method - Check if student is weak in this topic
     */
    public boolean isWeak() {
        return this.strengthLevel == StrengthLevel.WEAK;
    }

    /**
     * Business method - Check if student is strong
     */
    public boolean isStrong() {
        return this.strengthLevel == StrengthLevel.STRONG;
    }

    /**
     * Business method - Get confidence percentage
     */
    public double getConfidencePercentage() {
        return confidenceScore != null ? confidenceScore.doubleValue() * 100 : 0.0;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        WeaknessAnalysis that = (WeaknessAnalysis) o;
        return Objects.equals(analysisId, that.analysisId) &&
               Objects.equals(user, that.user) &&
               Objects.equals(topic, that.topic);
    }

    @Override
    public int hashCode() {
        return Objects.hash(analysisId, user, topic);
    }

    @Override
    public String toString() {
        return "WeaknessAnalysis{" +
               "analysisId=" + analysisId +
               ", strengthLevel=" + strengthLevel +
               ", confidenceScore=" + confidenceScore +
               ", avgScore=" + avgScore +
               ", totalAttempts=" + totalAttempts +
               ", lastAttemptDate=" + lastAttemptDate +
               ", analyzedAt=" + analyzedAt +
               '}';
    }
}