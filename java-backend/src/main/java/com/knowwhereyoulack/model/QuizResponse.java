package com.knowwhereyoulack.model;

import java.time.LocalDateTime;
import java.util.Objects;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;

/**
 * QuizResponse Entity
 * 
 * Represents a student's answer to a specific question in a quiz attempt
 */
@Entity
@Table(name = "quiz_responses")
public class QuizResponse {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "response_id")
    private Long responseId;

    @Column(name = "user_answer", length = 500)
    private String userAnswer;

    @Column(name = "is_correct", nullable = false)
    private Boolean isCorrect;

    @Column(name = "time_taken_seconds")
    private Integer timeTakenSeconds;

    @Column(name = "answered_at", nullable = false)
    private LocalDateTime answeredAt;

    // Many-to-One: Many Responses belong to One Attempt
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "attempt_id", nullable = false)
    private QuizAttempt attempt;

    // Many-to-One: Many Responses belong to One Question
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "question_id", nullable = false)
    private Question question;

    @PrePersist
    protected void onCreate() {
        if (answeredAt == null) {
            answeredAt = LocalDateTime.now();
        }
    }

    // Constructors
    public QuizResponse() {
    }

    public QuizResponse(Long responseId, String userAnswer, Boolean isCorrect, Integer timeTakenSeconds, 
                       LocalDateTime answeredAt, QuizAttempt attempt, Question question) {
        this.responseId = responseId;
        this.userAnswer = userAnswer;
        this.isCorrect = isCorrect;
        this.timeTakenSeconds = timeTakenSeconds;
        this.answeredAt = answeredAt;
        this.attempt = attempt;
        this.question = question;
    }

    // Getters and Setters
    public Long getResponseId() {
        return responseId;
    }

    public void setResponseId(Long responseId) {
        this.responseId = responseId;
    }

    public String getUserAnswer() {
        return userAnswer;
    }

    public void setUserAnswer(String userAnswer) {
        this.userAnswer = userAnswer;
    }

    public Boolean getIsCorrect() {
        return isCorrect;
    }

    public void setIsCorrect(Boolean isCorrect) {
        this.isCorrect = isCorrect;
    }

    public Integer getTimeTakenSeconds() {
        return timeTakenSeconds;
    }

    public void setTimeTakenSeconds(Integer timeTakenSeconds) {
        this.timeTakenSeconds = timeTakenSeconds;
    }

    public LocalDateTime getAnsweredAt() {
        return answeredAt;
    }

    public void setAnsweredAt(LocalDateTime answeredAt) {
        this.answeredAt = answeredAt;
    }

    public QuizAttempt getAttempt() {
        return attempt;
    }

    public void setAttempt(QuizAttempt attempt) {
        this.attempt = attempt;
    }

    public Question getQuestion() {
        return question;
    }

    public void setQuestion(Question question) {
        this.question = question;
    }

    // equals and hashCode
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        QuizResponse that = (QuizResponse) o;
        return Objects.equals(responseId, that.responseId) &&
               Objects.equals(userAnswer, that.userAnswer) &&
               Objects.equals(question, that.question);
    }

    @Override
    public int hashCode() {
        return Objects.hash(responseId, userAnswer, question);
    }

    @Override
    public String toString() {
        return "QuizResponse{" +
               "responseId=" + responseId +
               ", userAnswer='" + userAnswer + '\'' +
               ", isCorrect=" + isCorrect +
               ", timeTakenSeconds=" + timeTakenSeconds +
               ", answeredAt=" + answeredAt +
               '}';
    }
}