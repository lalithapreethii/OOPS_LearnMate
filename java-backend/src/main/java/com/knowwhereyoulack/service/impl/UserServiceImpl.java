package com.knowwhereyoulack.service.impl;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.knowwhereyoulack.config.JwtUtil;
import com.knowwhereyoulack.dto.LoginRequest;
import com.knowwhereyoulack.dto.RegisterRequest;
import com.knowwhereyoulack.exception.UnauthorizedException;
import com.knowwhereyoulack.exception.ValidationException;
import com.knowwhereyoulack.model.User;
import com.knowwhereyoulack.repository.UserRepository;
import com.knowwhereyoulack.service.UserService;

@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;

    public UserServiceImpl(UserRepository userRepository,
                           PasswordEncoder passwordEncoder,
                           JwtUtil jwtUtil) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
    }

    @Override
    public User register(RegisterRequest request) {
        // Spring validation will handle request field validation

        // Check if username already exists
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new ValidationException("Username already exists");
        }

        // Check if email already exists
        if (userRepository.existsByEmail(request.getEmail().toLowerCase().trim())) {
            throw new ValidationException("Email already exists");
        }

        // Create and initialize the user entity
        User user = new User();
        user.setUsername(request.getUsername());
        user.setFullName(request.getFullName());
        user.setEmail(request.getEmail().toLowerCase().trim());
        user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        user.setRole(User.UserRole.STUDENT); // Default role
        user.setIsActive(true);  // Active by default

        // Save and return the new user
        return userRepository.save(user);
    }

    @Override
    public String login(LoginRequest request) {
        // Spring validation will handle email and password validation

        // Find user by email and throw UnauthorizedException if not found
        User user = userRepository.findByEmail(request.getEmail().toLowerCase().trim())
                .orElseThrow(() -> new UnauthorizedException("Invalid email or password."));

        // Check if account is active
        if (!user.isAccountActive()) {
            throw new UnauthorizedException("Account is not active.");
        }

        // Verify password - keep the error message generic for security
        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new UnauthorizedException("Invalid email or password.");
        }

        // Generate JWT token and return it
        return jwtUtil.generateToken(user.getEmail());
    }
}