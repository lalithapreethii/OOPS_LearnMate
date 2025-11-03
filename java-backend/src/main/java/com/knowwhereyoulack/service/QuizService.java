package com.knowwhereyoulack.service;

import com.knowwhereyoulack.dto.TopicWithQuestionCount;
import com.knowwhereyoulack.model.Question;

import java.util.List;

public interface QuizService {
    
    List<TopicWithQuestionCount> getAllTopicsWithQuestionCount();
    
    List<Question> getQuestionsByTopicAndDifficulty(Long topicId, String difficulty);
    
    List<Question> getAllQuestionsByTopic(Long topicId);
}
