package com.knowwhereyoulack.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.knowwhereyoulack.model.User;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
    boolean existsByUsername(String username);
}
