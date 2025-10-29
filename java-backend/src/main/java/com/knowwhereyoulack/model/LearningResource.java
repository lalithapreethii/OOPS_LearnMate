package com.knowwhereyoulack.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * LearningResource Entity
 * 
 * Represents a learning resource (video, article, practice problem)
 * recommended for a topic
 */
@Entity
@Table(name = "learning_resources")
public class LearningResource {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "resource_id")
    private Long resourceId;

    @Enumerated(EnumType.STRING)
    @Column(name = "resource_type", nullable = false)
    private ResourceType resourceType;

    @Column(name = "title", nullable = false)
    private String title;

    @Column(name = "url", nullable = false, length = 500)
    private String url;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(name = "difficulty_level")
    private DifficultyLevel difficultyLevel = DifficultyLevel.INTERMEDIATE;

    @Column(name = "duration_minutes")
    private Integer durationMinutes;

    @Column(name = "relevance_score", precision = 3, scale = 2)
    private BigDecimal relevanceScore = BigDecimal.valueOf(0.80);

    @Column(name = "is_active")
    private Boolean isActive = true;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    // Many-to-One: Many Resources belong to One Topic
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "topic_id", nullable = false)
    private Topic topic;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    /**
     * Enum for Resource Types
     */
    public enum ResourceType {
        VIDEO,
        ARTICLE,
        PRACTICE,
        BOOK
    }

    /**
     * Enum for Difficulty Levels
     */
    public enum DifficultyLevel {
        BEGINNER,
        INTERMEDIATE,
        ADVANCED
    }

    // Constructors
    public LearningResource() {
    }

    public LearningResource(Long resourceId, ResourceType resourceType, String title, String url, 
                           String description, DifficultyLevel difficultyLevel, Integer durationMinutes,
                           BigDecimal relevanceScore, Boolean isActive, LocalDateTime createdAt, Topic topic) {
        this.resourceId = resourceId;
        this.resourceType = resourceType;
        this.title = title;
        this.url = url;
        this.description = description;
        this.difficultyLevel = difficultyLevel;
        this.durationMinutes = durationMinutes;
        this.relevanceScore = relevanceScore;
        this.isActive = isActive;
        this.createdAt = createdAt;
        this.topic = topic;
    }

    // Getters and Setters
    public Long getResourceId() {
        return resourceId;
    }

    public void setResourceId(Long resourceId) {
        this.resourceId = resourceId;
    }

    public ResourceType getResourceType() {
        return resourceType;
    }

    public void setResourceType(ResourceType resourceType) {
        this.resourceType = resourceType;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public DifficultyLevel getDifficultyLevel() {
        return difficultyLevel;
    }

    public void setDifficultyLevel(DifficultyLevel difficultyLevel) {
        this.difficultyLevel = difficultyLevel;
    }

    public Integer getDurationMinutes() {
        return durationMinutes;
    }

    public void setDurationMinutes(Integer durationMinutes) {
        this.durationMinutes = durationMinutes;
    }

    public BigDecimal getRelevanceScore() {
        return relevanceScore;
    }

    public void setRelevanceScore(BigDecimal relevanceScore) {
        this.relevanceScore = relevanceScore;
    }

    public Boolean getIsActive() {
        return isActive;
    }

    public void setIsActive(Boolean isActive) {
        this.isActive = isActive;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public Topic getTopic() {
        return topic;
    }

    public void setTopic(Topic topic) {
        this.topic = topic;
    }

    /**
     * Business method - Check if resource is video
     */
    public boolean isVideo() {
        return this.resourceType == ResourceType.VIDEO;
    }

    /**
     * Business method - Get relevance percentage
     */
    public double getRelevancePercentage() {
        return relevanceScore != null ? relevanceScore.doubleValue() * 100 : 80.0;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        LearningResource that = (LearningResource) o;
        return Objects.equals(resourceId, that.resourceId) &&
               Objects.equals(title, that.title);
    }

    @Override
    public int hashCode() {
        return Objects.hash(resourceId, title);
    }

    @Override
    public String toString() {
        return "LearningResource{" +
               "resourceId=" + resourceId +
               ", resourceType=" + resourceType +
               ", title='" + title + '\'' +
               ", url='" + url + '\'' +
               ", difficultyLevel=" + difficultyLevel +
               ", durationMinutes=" + durationMinutes +
               ", relevanceScore=" + relevanceScore +
               ", isActive=" + isActive +
               '}';
    }
}