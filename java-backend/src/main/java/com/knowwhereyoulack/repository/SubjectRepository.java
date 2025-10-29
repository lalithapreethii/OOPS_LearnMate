package com.knowwhereyoulack.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.knowwhereyoulack.model.Subject;

public interface SubjectRepository extends JpaRepository<Subject, Long> {
}