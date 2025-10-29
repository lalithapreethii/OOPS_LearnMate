package com.knowwhereyoulack.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Subject Entity - Demonstrates OOP Relationships (One-to-Many)
 * 
 * Represents an academic subject (e.g., Data Structures, Algorithms)
 */
@Entity
@Table(name = "subjects")
public class Subject {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "subject_id")
    private Long subjectId;

    @Column(name = "subject_name", nullable = false, length = 100)
    private String subjectName;

    @Column(name = "subject_code", unique = true, nullable = false, length = 20)
    private String subjectCode;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    // One-to-Many Relationship: One Subject has Many Topics
    @OneToMany(mappedBy = "subject", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private final List<Topic> topics = new ArrayList<>();

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getSubjectId() {
        return subjectId;
    }

    public void setSubjectId(Long subjectId) {
        this.subjectId = subjectId;
    }

    public String getSubjectName() {
        return subjectName;
    }

    public void setSubjectName(String subjectName) {
        this.subjectName = subjectName;
    }

    public String getSubjectCode() {
        return subjectCode;
    }

    public void setSubjectCode(String subjectCode) {
        this.subjectCode = subjectCode;
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

    public List<Topic> getTopics() {
        return topics;
    }

    /**
     * Business method - Add topic to subject
     * Demonstrates OOP: Managing relationships
     */
    public void addTopic(Topic topic) {
        topics.add(topic);
        topic.setSubject(this);
    }

    /**
     * Business method - Remove topic from subject
     */
    public void removeTopic(Topic topic) {
        topics.remove(topic);
        topic.setSubject(null);
    }

    /**
     * Business method - Get total number of topics
     */
    public int getTopicCount() {
        return topics != null ? topics.size() : 0;
    }
}