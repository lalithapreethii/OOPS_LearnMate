package com.knowwhereyoulack.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * DTO used for user registration requests.
 * Includes Jakarta Validation annotations; ensure you have
 * spring-boot-starter-validation on the classpath.
 */
public class RegisterRequest {

    @NotBlank(message = "username is required")
    @Size(max = 50, message = "username must be <= 50 chars")
    private String username;

    @NotBlank(message = "fullName is required")
    @Size(max = 100, message = "fullName must be <= 100 chars")
    private String fullName;

    @NotBlank(message = "email is required")
    @Email(message = "email must be valid")
    @Size(max = 100, message = "email must be <= 100 chars")
    private String email;

    @NotBlank(message = "password is required")
    @Size(min = 6, max = 100, message = "password must be between 6 and 100 chars")
    private String password;

    /**
     * Optional - one of: STUDENT, TEACHER, ADMIN
     * If omitted, service can default to STUDENT.
     */
    private String role;

    // No-arg constructor
    public RegisterRequest() {}

    // All-args constructor
    public RegisterRequest(String username, String fullName, String email, String password, String role) {
        this.username = username;
        this.fullName = fullName;
        this.email = email;
        this.password = password;
        this.role = role;
    }

    // Getters & Setters
    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }
}
