package com.knowwhereyoulack.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.knowwhereyoulack.model.Question;
import com.knowwhereyoulack.model.Topic;

public interface QuestionRepository extends JpaRepository<Question, Long> {
    List<Question> findByTopic(Topic topic);
}
