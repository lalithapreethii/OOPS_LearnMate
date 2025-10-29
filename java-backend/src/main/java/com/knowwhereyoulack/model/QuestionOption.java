package com.knowwhereyoulack.model;

import java.util.Objects;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

/**
 * QuestionOption Entity
 * 
 * Represents an option for a multiple-choice question
 */
@Entity
@Table(name = "question_options")
public class QuestionOption {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "option_id")
    private Long optionId;

    @Column(name = "option_text", nullable = false, length = 500)
    private String optionText;

    @Column(name = "option_label", nullable = false, length = 10)
    private String optionLabel;  // A, B, C, D

    @Column(name = "is_correct")
    private Boolean isCorrect = false;

    // Many-to-One: Many Options belong to One Question
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "question_id", nullable = false)
    private Question question;

    /**
     * Business method - Check if this option is the correct answer
     */
    public boolean isCorrectOption() {
        return isCorrect != null && isCorrect;
    }

    // Constructors
    public QuestionOption() {
    }

    public QuestionOption(Long optionId, String optionText, String optionLabel, Boolean isCorrect, Question question) {
        this.optionId = optionId;
        this.optionText = optionText;
        this.optionLabel = optionLabel;
        this.isCorrect = isCorrect;
        this.question = question;
    }

    // Getters and Setters
    public Long getOptionId() {
        return optionId;
    }

    public void setOptionId(Long optionId) {
        this.optionId = optionId;
    }

    public String getOptionText() {
        return optionText;
    }

    public void setOptionText(String optionText) {
        this.optionText = optionText;
    }

    public String getOptionLabel() {
        return optionLabel;
    }

    public void setOptionLabel(String optionLabel) {
        this.optionLabel = optionLabel;
    }

    public Boolean getIsCorrect() {
        return isCorrect;
    }

    public void setIsCorrect(Boolean isCorrect) {
        this.isCorrect = isCorrect;
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
        QuestionOption that = (QuestionOption) o;
        return Objects.equals(optionId, that.optionId) &&
               Objects.equals(optionText, that.optionText);
    }

    @Override
    public int hashCode() {
        return Objects.hash(optionId, optionText);
    }

    @Override
    public String toString() {
        return "QuestionOption{" +
               "optionId=" + optionId +
               ", optionText='" + optionText + '\'' +
               ", optionLabel='" + optionLabel + '\'' +
               ", isCorrect=" + isCorrect +
               '}';
    }
}