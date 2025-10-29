package com.knowwhereyoulack.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.knowwhereyoulack.model.LearningResource;
import com.knowwhereyoulack.model.Topic;

public interface LearningResourceRepository extends JpaRepository<LearningResource, Long> {
    List<LearningResource> findByTopic(Topic topic);
}
