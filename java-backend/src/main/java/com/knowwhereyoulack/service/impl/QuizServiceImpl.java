package com.knowwhereyoulack.service.impl;

import java.util.List;

import org.springframework.stereotype.Service;

import com.knowwhereyoulack.dto.AnswerRequest;
import com.knowwhereyoulack.dto.QuizResponseDto;
import com.knowwhereyoulack.dto.QuizSubmissionRequest;
import com.knowwhereyoulack.exception.ResourceNotFoundException;
import com.knowwhereyoulack.model.Question;
import com.knowwhereyoulack.model.QuizAttempt;
import com.knowwhereyoulack.model.Topic;
import com.knowwhereyoulack.repository.QuestionRepository;
import com.knowwhereyoulack.repository.QuizAttemptRepository;
import com.knowwhereyoulack.repository.TopicRepository;
import com.knowwhereyoulack.service.QuizService;

@Service
public class QuizServiceImpl implements QuizService {

    private final TopicRepository topicRepository;
    private final QuestionRepository questionRepository;
    private final QuizAttemptRepository quizAttemptRepository;

    public QuizServiceImpl(TopicRepository topicRepository,
                           QuestionRepository questionRepository,
                           QuizAttemptRepository quizAttemptRepository) {
        this.topicRepository = topicRepository;
        this.questionRepository = questionRepository;
        this.quizAttemptRepository = quizAttemptRepository;
    }

    @Override
    public List<Topic> getAllTopics() {
        return topicRepository.findAll();
    }

    @Override
    public QuizResponseDto generateQuiz(Long topicId, Long userId) {
        Topic topic = topicRepository.findById(topicId)
                .orElseThrow(() -> new ResourceNotFoundException("Topic not found"));

        List<Question> questions = questionRepository.findByTopic(topic);

        return new QuizResponseDto(topic.getTopicId(), topic.getTopicName(), questions);
    }

    @Override
    public String submitQuiz(QuizSubmissionRequest request) {
        QuizAttempt attempt = new QuizAttempt();
        attempt.setTotalQuestions(request.getAnswers().size());
        int correct = 0;

        for (AnswerRequest ans : request.getAnswers()) {
            Question question = questionRepository.findById(ans.getQuestionId())
                    .orElseThrow(() -> new ResourceNotFoundException("Question not found"));

            if (question.isCorrectAnswer(ans.getSelectedAnswer())) {
                correct++;
            }
        }

        attempt.setCorrectAnswers(correct);
        attempt.calculateScore();
        quizAttemptRepository.save(attempt);

        return "Quiz submitted successfully. Score: " + attempt.getScorePercentage() + "%";
    }
}
