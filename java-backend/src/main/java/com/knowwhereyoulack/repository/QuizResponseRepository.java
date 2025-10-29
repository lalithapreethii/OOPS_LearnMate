package com.knowwhereyoulack.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.knowwhereyoulack.model.QuizResponse;

public interface QuizResponseRepository extends JpaRepository<QuizResponse, Long> {
}
