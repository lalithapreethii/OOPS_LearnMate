package com.knowwhereyoulack.repository;

import com.knowwhereyoulack.model.QuizResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface QuizResultRepository extends JpaRepository<QuizResult, Long> {
    List<QuizResult> findByUserIdOrderByCompletedAtDesc(Long userId);
    
    @Query("SELECT AVG(r.accuracy) FROM QuizResult r WHERE r.userId = ?1")
    Double getAverageAccuracyByUserId(Long userId);
    
    @Query("SELECT r.topic, AVG(r.accuracy), COUNT(r) FROM QuizResult r WHERE r.userId = ?1 GROUP BY r.topic")
    List<Object[]> getTopicPerformanceByUserId(Long userId);
    
    @Query("SELECT COUNT(r) FROM QuizResult r WHERE r.userId = ?1")
    Long getTotalQuizzesByUserId(Long userId);
}
