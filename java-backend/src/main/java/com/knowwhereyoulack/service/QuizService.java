package com.knowwhereyoulack.service;

import com.knowwhereyoulack.dto.QuizSubmissionRequest;
import com.knowwhereyoulack.dto.QuizResponseDto;
import com.knowwhereyoulack.model.Topic;
import java.util.List;

public interface QuizService {
    List<Topic> getAllTopics();
    QuizResponseDto generateQuiz(Long topicId, Long userId);
    String submitQuiz(QuizSubmissionRequest request);
}