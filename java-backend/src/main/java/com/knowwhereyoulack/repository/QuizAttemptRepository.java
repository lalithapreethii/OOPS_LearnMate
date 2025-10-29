package com.knowwhereyoulack.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.knowwhereyoulack.model.QuizAttempt;
import com.knowwhereyoulack.model.User;

public interface QuizAttemptRepository extends JpaRepository<QuizAttempt, Long> {
    List<QuizAttempt> findByUser(User user);
    List<QuizAttempt> findByUser_UserId(Long userId);
}
