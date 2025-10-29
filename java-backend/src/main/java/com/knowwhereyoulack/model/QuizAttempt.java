package com.knowwhereyoulack.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;

/**
 * Entity class representing a quiz attempt made by a user
 */
@Entity
@Table(name = "quiz_attempts")
public class QuizAttempt {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "attempt_id")
    private Long attemptId;

    @Column(name = "total_questions", nullable = false)
    private Integer totalQuestions;

    @Column(name = "correct_answers", nullable = false)
    private Integer correctAnswers;

    @Column(name = "score_percentage", nullable = false, precision = 5, scale = 2)
    private BigDecimal scorePercentage;

    @Column(name = "time_taken_seconds", nullable = false)
    private Integer timeTakenSeconds;

    @Column(name = "started_at", nullable = false)
    private LocalDateTime startedAt;

    @Column(name = "completed_at", nullable = false)
    private LocalDateTime completedAt;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "topic_id", nullable = false)
    private Topic topic;

    @OneToMany(mappedBy = "attempt", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<QuizResponse> responses = new ArrayList<>();

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    public void calculateScore() {
        if (totalQuestions > 0) {
            double percentage = (correctAnswers.doubleValue() / totalQuestions.doubleValue()) * 100;
            this.scorePercentage = BigDecimal.valueOf(percentage);
        } else {
            this.scorePercentage = BigDecimal.ZERO;
        }
    }

    public boolean isPassed() {
        return scorePercentage != null && scorePercentage.compareTo(BigDecimal.valueOf(60)) >= 0;
    }

    public String getPerformanceLevel() {
        if (scorePercentage == null) return "UNKNOWN";
        
        double score = scorePercentage.doubleValue();
        if (score >= 80) return "STRONG";
        else if (score >= 60) return "MODERATE";
        else return "WEAK";
    }

    public QuizAttempt() {
    }

    public QuizAttempt(Long attemptId, Integer totalQuestions, Integer correctAnswers, BigDecimal scorePercentage,
                      Integer timeTakenSeconds, LocalDateTime startedAt, LocalDateTime completedAt,
                      LocalDateTime createdAt, User user, Topic topic, List<QuizResponse> responses) {
        this.attemptId = attemptId;
        this.totalQuestions = totalQuestions;
        this.correctAnswers = correctAnswers;
        this.scorePercentage = scorePercentage;
        this.timeTakenSeconds = timeTakenSeconds;
        this.startedAt = startedAt;
        this.completedAt = completedAt;
        this.createdAt = createdAt;
        this.user = user;
        this.topic = topic;
        this.responses = responses != null ? responses : new ArrayList<>();
    }

    // Getters and Setters
    public Long getAttemptId() {
        return attemptId;
    }

    public void setAttemptId(Long attemptId) {
        this.attemptId = attemptId;
    }

    public Integer getTotalQuestions() {
        return totalQuestions;
    }

    public void setTotalQuestions(Integer totalQuestions) {
        this.totalQuestions = totalQuestions;
    }

    public Integer getCorrectAnswers() {
        return correctAnswers;
    }

    public void setCorrectAnswers(Integer correctAnswers) {
        this.correctAnswers = correctAnswers;
    }

    public BigDecimal getScorePercentage() {
        return scorePercentage;
    }

    public void setScorePercentage(BigDecimal scorePercentage) {
        this.scorePercentage = scorePercentage;
    }

    public Integer getTimeTakenSeconds() {
        return timeTakenSeconds;
    }

    public void setTimeTakenSeconds(Integer timeTakenSeconds) {
        this.timeTakenSeconds = timeTakenSeconds;
    }

    public LocalDateTime getStartedAt() {
        return startedAt;
    }

    public void setStartedAt(LocalDateTime startedAt) {
        this.startedAt = startedAt;
    }

    public LocalDateTime getCompletedAt() {
        return completedAt;
    }

    public void setCompletedAt(LocalDateTime completedAt) {
        this.completedAt = completedAt;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
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

    public List<QuizResponse> getResponses() {
        return responses;
    }

    public void setResponses(List<QuizResponse> responses) {
        this.responses = responses;
    }

    public void addResponse(QuizResponse response) {
        responses.add(response);
        response.setAttempt(this);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        QuizAttempt that = (QuizAttempt) o;
        return Objects.equals(attemptId, that.attemptId) &&
               Objects.equals(user, that.user) &&
               Objects.equals(topic, that.topic);
    }

    @Override
    public int hashCode() {
        return Objects.hash(attemptId, user, topic);
    }

    @Override
    public String toString() {
        return "QuizAttempt{" +
               "attemptId=" + attemptId +
               ", totalQuestions=" + totalQuestions +
               ", correctAnswers=" + correctAnswers +
               ", scorePercentage=" + scorePercentage +
               ", timeTakenSeconds=" + timeTakenSeconds +
               ", startedAt=" + startedAt +
               ", completedAt=" + completedAt +
               '}';
    }
}
