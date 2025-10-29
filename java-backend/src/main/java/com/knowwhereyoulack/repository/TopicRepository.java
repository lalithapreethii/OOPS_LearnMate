package com.knowwhereyoulack.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.knowwhereyoulack.model.Topic;

public interface TopicRepository extends JpaRepository<Topic, Long> {
    List<Topic> findBySubject_SubjectId(Long subjectId);
}
