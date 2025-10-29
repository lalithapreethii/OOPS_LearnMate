package com.knowwhereyoulack.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.knowwhereyoulack.model.WeaknessAnalysis;

public interface WeaknessAnalysisRepository extends JpaRepository<WeaknessAnalysis, Long> {
    List<WeaknessAnalysis> findByUser_UserId(Long userId);
}
