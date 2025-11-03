package com.knowwhereyoulack.dto;

import com.knowwhereyoulack.model.Topic.DifficultyLevel;

public class TopicWithQuestionCount {
    private Long topicId;
    private String topicName;
    private DifficultyLevel difficultyLevel;
    private String description;
    private Long questionCount;

    // Default Constructor
    public TopicWithQuestionCount() {}

    // Full Constructor
    public TopicWithQuestionCount(Long topicId, String topicName, 
                                   DifficultyLevel difficultyLevel, 
                                   String description, Long questionCount) {
        this.topicId = topicId;
        this.topicName = topicName;
        this.difficultyLevel = difficultyLevel;
        this.description = description;
        this.questionCount = questionCount;
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

    public Long getQuestionCount() {
        return questionCount;
    }

    public void setQuestionCount(Long questionCount) {
        this.questionCount = questionCount;
    }
}
