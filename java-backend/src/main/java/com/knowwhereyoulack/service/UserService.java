package com.knowwhereyoulack.service;

import com.knowwhereyoulack.dto.LoginRequest;
import com.knowwhereyoulack.dto.RegisterRequest;
import com.knowwhereyoulack.model.User;

public interface UserService {
    /**
     * Register a new user with the system.
     *
     * @param request The registration details
     * @return The newly created user
     */
    User register(RegisterRequest request);

    /**
     * Authenticate a user and generate a JWT token.
     *
     * @param request The login credentials
     * @return JWT token string
     */
    String login(LoginRequest request);
}