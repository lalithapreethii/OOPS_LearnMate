package com.knowwhereyoulack.service.impl;

import com.knowwhereyoulack.dto.TopicWithQuestionCount;
import com.knowwhereyoulack.model.Question;
import com.knowwhereyoulack.model.Topic;
import com.knowwhereyoulack.repository.QuestionRepository;
import com.knowwhereyoulack.repository.TopicRepository;
import com.knowwhereyoulack.service.QuizService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class QuizServiceImpl implements QuizService {
    
    private final QuestionRepository questionRepository;
    private final TopicRepository topicRepository;
    
    @Autowired
    public QuizServiceImpl(QuestionRepository questionRepository, 
                           TopicRepository topicRepository) {
        this.questionRepository = questionRepository;
        this.topicRepository = topicRepository;
    }
    
    @Override
    public List<TopicWithQuestionCount> getAllTopicsWithQuestionCount() {
        List<Topic> topics = topicRepository.findAllByOrderByTopicIdAsc();
        
        return topics.stream()
            .map(topic -> {
                // Use countByTopicId method from QuestionRepository
                Long questionCount = questionRepository.countByTopicId(topic.getTopicId());
                return new TopicWithQuestionCount(
                    topic.getTopicId(),
                    topic.getTopicName(),
                    topic.getDifficultyLevel(),
                    topic.getDescription(),
                    questionCount != null ? questionCount : 0L
                );
            })
            .collect(Collectors.toList());
    }
    
    @Override
    public List<Question> getQuestionsByTopicAndDifficulty(Long topicId, String difficulty) {
        System.out.println("🔍 QuizServiceImpl.getQuestionsByTopicAndDifficulty called");
        System.out.println("   Topic ID: " + topicId);
        System.out.println("   Difficulty: " + difficulty);
        
        // Use findRandomQuestionsByTopicAndDifficulty from QuestionRepository
        List<Question> questions = questionRepository.findRandomQuestionsByTopicAndDifficulty(
            topicId, 
            difficulty.toUpperCase()
        );
        
        System.out.println("   Questions found: " + questions.size());
        
        return questions;
    }
    
    @Override
    public List<Question> getAllQuestionsByTopic(Long topicId) {
        // FIXED: Changed from findByTopicTopicId to findByTopicId
        return questionRepository.findByTopicId(topicId);
    }
}
