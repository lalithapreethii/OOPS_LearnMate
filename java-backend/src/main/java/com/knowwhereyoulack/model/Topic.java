package com.knowwhereyoulack.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Topic Entity - Demonstrates OOP Relationships (Many-to-One)
 * 
 * Represents a topic within a subject (e.g., Arrays, Linked Lists)
 *
 * Note: Lombok removed due to Java 21 compatibility issues
 */
@Entity
@Table(name = "topics")
public class Topic {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "topic_id")
    private Long topicId;

    @Column(name = "topic_name", nullable = false, length = 150)
    private String topicName;

    @Column(name = "topic_order")
    private Integer topicOrder = 0;

    @Enumerated(EnumType.STRING)
    @Column(name = "difficulty_level")
    private DifficultyLevel difficultyLevel = DifficultyLevel.MEDIUM;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    // Many-to-One Relationship: Many Topics belong to One Subject
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "subject_id", nullable = false)
    private Subject subject;

    // One-to-Many: One Topic has Many Questions
    @OneToMany(mappedBy = "topic", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Question> questions = new ArrayList<>();

    // One-to-Many: One Topic has Many Quiz Attempts
    @OneToMany(mappedBy = "topic", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<QuizAttempt> attempts = new ArrayList<>();

    // One-to-Many: One Topic has Many Weakness Analyses
    @OneToMany(mappedBy = "topic", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<WeaknessAnalysis> weaknessAnalyses = new ArrayList<>();


    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getTopicId() {
        return topicId;
    }

    public void setTopicId(Long topicId) {
        this.topicId = topicId;
    }

    public String getTopicName() {
        return topicName;
    }

    public void setTopicName(String topicName) {
        this.topicName = topicName;
    }

    public Integer getTopicOrder() {
        return topicOrder;
    }

    public void setTopicOrder(Integer topicOrder) {
        this.topicOrder = topicOrder;
    }

    public DifficultyLevel getDifficultyLevel() {
        return difficultyLevel;
    }

    public void setDifficultyLevel(DifficultyLevel difficultyLevel) {
        this.difficultyLevel = difficultyLevel;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public Subject getSubject() {
        return subject;
    }

    public void setSubject(Subject subject) {
        this.subject = subject;
    }

    public List<Question> getQuestions() {
        return questions;
    }

    public void setQuestions(List<Question> questions) {
        this.questions = questions;
    }

    public List<QuizAttempt> getAttempts() {
        return attempts;
    }

    public void setAttempts(List<QuizAttempt> attempts) {
        this.attempts = attempts;
    }

    public List<WeaknessAnalysis> getWeaknessAnalyses() {
        return weaknessAnalyses;
    }

    public void setWeaknessAnalyses(List<WeaknessAnalysis> weaknessAnalyses) {
        this.weaknessAnalyses = weaknessAnalyses;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Topic topic = (Topic) o;
        return Objects.equals(topicId, topic.topicId) &&
               Objects.equals(topicName, topic.topicName);
    }

    @Override
    public int hashCode() {
        return Objects.hash(topicId, topicName);
    }

    @Override
    public String toString() {
        return "Topic{" +
               "topicId=" + topicId +
               ", topicName='" + topicName + '\'' +
               ", topicOrder=" + topicOrder +
               ", difficultyLevel=" + difficultyLevel +
               ", description='" + description + '\'' +
               ", createdAt=" + createdAt +
               '}';
    }

    /**
     * Enum for Difficulty Levels
     */
    public enum DifficultyLevel {
        EASY,
        MEDIUM,
        HARD
    }

    /**
     * Business method - Check if topic is difficult
     */
    public boolean isDifficult() {
        return this.difficultyLevel == DifficultyLevel.HARD;
    }
}