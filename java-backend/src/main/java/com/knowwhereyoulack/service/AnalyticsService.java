package com.knowwhereyoulack.service;

import com.knowwhereyoulack.model.QuizResult;
import com.knowwhereyoulack.model.WeakTopic;
import com.knowwhereyoulack.repository.QuizResultRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.ZoneId;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class AnalyticsService {
    
    @Autowired
    private QuizResultRepository quizResultRepository;
    
    public List<WeakTopic> getWeakTopics(Long userId) {
        List<Object[]> topicData = quizResultRepository.getTopicPerformanceByUserId(userId);
        
        return topicData.stream()
            .map(data -> new WeakTopic(
                (String) data[0],           // topic
                (Double) data[1],           // average accuracy
                ((Long) data[2]).intValue() // total attempts
            ))
            .filter(topic -> topic.getCurrentScore() < 80.0) // Only weak topics
            .sorted(Comparator.comparing(WeakTopic::getCurrentScore))
            .limit(4)
            .collect(Collectors.toList());
    }
    
    public Double getAverageAccuracy(Long userId) {
        Double avg = quizResultRepository.getAverageAccuracyByUserId(userId);
        return avg != null ? Math.round(avg * 10.0) / 10.0 : 0.0;
    }
    
    public Long getTotalQuizzes(Long userId) {
        return quizResultRepository.getTotalQuizzesByUserId(userId);
    }
    
    public Integer getWeeklyStreak(Long userId) {
        List<QuizResult> results = quizResultRepository.findByUserIdOrderByCompletedAtDesc(userId);
        
        if (results.isEmpty()) return 0;
        
        Set<LocalDate> uniqueDays = results.stream()
            .map(result -> result.getCompletedAt().toInstant()
                .atZone(ZoneId.systemDefault()).toLocalDate())
            .collect(Collectors.toSet());
        
        LocalDate today = LocalDate.now();
        int streak = 0;
        
        for (int i = 0; i < 7; i++) {
            if (uniqueDays.contains(today.minusDays(i))) {
                streak++;
            }
        }
        
        return streak;
    }
    
    public List<Map<String, Object>> getRecentQuizAccuracy(Long userId) {
        List<QuizResult> results = quizResultRepository.findByUserIdOrderByCompletedAtDesc(userId);
        
        return results.stream()
            .limit(5)
            .map(result -> {
                Map<String, Object> map = new HashMap<>();
                map.put("name", "Quiz " + result.getId());
                map.put("accuracy", result.getAccuracy());
                return map;
            })
            .collect(Collectors.toList());
    }
    
    public void saveQuizResult(Map<String, Object> quizData) {
        QuizResult result = new QuizResult();
        result.setUserId(((Number) quizData.get("userId")).longValue());
        result.setTopic((String) quizData.get("topic"));
        result.setScore(((Number) quizData.get("score")).intValue());
        result.setTotalQuestions(((Number) quizData.get("totalQuestions")).intValue());
        result.setCompletedAt(new Date());
        
        quizResultRepository.save(result);
    }
}
