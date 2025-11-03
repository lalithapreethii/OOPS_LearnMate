package com.knowwhereyoulack.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.knowwhereyoulack.model.Question;
import com.knowwhereyoulack.model.Topic;

@Repository
public interface QuestionRepository extends JpaRepository<Question, Long> {
    
    // ========== EXISTING METHODS (KEEP THESE) ==========
    
    /**
     * Find all questions for a specific topic
     */
    List<Question> findByTopic(Topic topic);
    
    /**
     * Find questions by topic and difficulty level
     */
    List<Question> findByTopicAndDifficultyLevel(Topic topic, String difficultyLevel);
    
    /**
     * Find random 10 questions by topic and difficulty level
     */
    @Query(value = "SELECT * FROM questions WHERE topic_id = :topicId " +
                   "AND difficulty_level = :difficulty " +
                   "AND is_active = true " +
                   "ORDER BY RAND() LIMIT 10", 
           nativeQuery = true)
    List<Question> findRandomQuestionsByTopicAndDifficulty(
        @Param("topicId") Long topicId, 
        @Param("difficulty") String difficulty
    );
    
    /**
     * Find random 10 questions by topic only (any difficulty)
     */
    @Query(value = "SELECT * FROM questions WHERE topic_id = :topicId " +
                   "AND is_active = true " +
                   "ORDER BY RAND() LIMIT 10", 
           nativeQuery = true)
    List<Question> findRandomQuestionsByTopic(@Param("topicId") Long topicId);
    
    
    // ========== NEW METHODS (ADD THESE) ==========
    
    /**
     * Find all questions by topic ID (using topic_id directly)
     */
    @Query(value = "SELECT * FROM questions WHERE topic_id = :topicId " +
                   "AND is_active = true", 
           nativeQuery = true)
    List<Question> findByTopicId(@Param("topicId") Long topicId);
    
    /**
     * Count total questions for a specific topic
     */
    @Query(value = "SELECT COUNT(*) FROM questions WHERE topic_id = :topicId " +
                   "AND is_active = true", 
           nativeQuery = true)
    Long countByTopicId(@Param("topicId") Long topicId);
    
    /**
     * Count questions by topic and difficulty
     */
    @Query(value = "SELECT COUNT(*) FROM questions WHERE topic_id = :topicId " +
                   "AND difficulty_level = :difficulty " +
                   "AND is_active = true", 
           nativeQuery = true)
    Long countByTopicIdAndDifficulty(
        @Param("topicId") Long topicId, 
        @Param("difficulty") String difficulty
    );
}
