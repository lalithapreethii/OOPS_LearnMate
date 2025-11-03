package com.knowwhereyoulack.controller;

import com.knowwhereyoulack.dto.QuizResponseDto;
import com.knowwhereyoulack.dto.TopicWithQuestionCount;
import com.knowwhereyoulack.model.Question;
import com.knowwhereyoulack.model.Topic;
import com.knowwhereyoulack.repository.TopicRepository;
import com.knowwhereyoulack.service.QuizService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/quiz")
@CrossOrigin(origins = "http://localhost:5173")
public class QuizController {
    
    private final QuizService quizService;
    private final TopicRepository topicRepository;
    
    @Autowired
    public QuizController(QuizService quizService, TopicRepository topicRepository) {
        this.quizService = quizService;
        this.topicRepository = topicRepository;
    }
    
    /**
     * Get all topics with question counts
     */
    @GetMapping("/topics")
    public ResponseEntity<List<TopicWithQuestionCount>> getAllTopics() {
        try {
            List<TopicWithQuestionCount> topics = quizService.getAllTopicsWithQuestionCount();
            return ResponseEntity.ok(topics);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * Get questions by topic and difficulty level
     * Returns QuizResponseDto with topic info and 10 random questions
     */
    @GetMapping("/{topicId}/difficulty/{difficulty}")
    public ResponseEntity<QuizResponseDto> getQuestionsByDifficulty(
            @PathVariable Long topicId,
            @PathVariable String difficulty) {
        
        try {
            // Get the topic details
            Optional<Topic> topicOptional = topicRepository.findById(topicId);
            if (!topicOptional.isPresent()) {
                return ResponseEntity.notFound().build();
            }
            
            Topic topic = topicOptional.get();
            
            // Get 10 random questions for this topic and difficulty
            List<Question> questions = quizService.getQuestionsByTopicAndDifficulty(
                topicId, 
                difficulty.toUpperCase()
            );
            
            // Create response DTO
            QuizResponseDto response = new QuizResponseDto(
                topic.getTopicId(),
                topic.getTopicName(),
                questions
            );
            
            if (questions.isEmpty()) {
                System.out.println("⚠️ WARNING: No questions found for topic " + topicId + 
                                 " with difficulty " + difficulty);
            } else {
                System.out.println("✅ Returning " + questions.size() + " questions for topic " + 
                                 topicId + " with difficulty " + difficulty);
            }
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            System.err.println("❌ ERROR in getQuestionsByDifficulty: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    /**
     * Get all questions for a topic
     */
    @GetMapping("/{topicId}/questions")
    public ResponseEntity<List<Question>> getAllQuestions(@PathVariable Long topicId) {
        try {
            List<Question> questions = quizService.getAllQuestionsByTopic(topicId);
            return ResponseEntity.ok(questions);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
