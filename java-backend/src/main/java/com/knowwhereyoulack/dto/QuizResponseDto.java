package com.knowwhereyoulack.dto;

import java.util.List;

import com.knowwhereyoulack.model.Question;

public class QuizResponseDto {
    private Long topicId;
    private String topicName;
    private List<Question> questions;

    public QuizResponseDto(Long topicId, String topicName, List<Question> questions) {
        this.topicId = topicId;
        this.topicName = topicName;
        this.questions = questions;
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

    public List<Question> getQuestions() {
        return questions;
    }

    public void setQuestions(List<Question> questions) {
        this.questions = questions;
    }
}