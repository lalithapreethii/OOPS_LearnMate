package com.knowwhereyoulack.controller;

import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.knowwhereyoulack.dto.LoginRequest;
import com.knowwhereyoulack.dto.RegisterRequest;
import com.knowwhereyoulack.dto.UserResponse;
import com.knowwhereyoulack.model.User;
import com.knowwhereyoulack.repository.UserRepository;
import com.knowwhereyoulack.service.UserService;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = {"http://localhost:5173"}, maxAge = 3600)
public class AuthController {

    private final UserService userService;
    private final UserRepository userRepository;

    public AuthController(UserService userService, UserRepository userRepository) {
        this.userService = userService;
        this.userRepository = userRepository;
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@Validated @RequestBody RegisterRequest req) {
        try {
            User created = userService.register(req);
            UserResponse resp = new UserResponse();
            resp.setUserId(created.getUserId());
            resp.setName(created.getFullName());
            resp.setEmail(created.getEmail());
            return ResponseEntity.ok(resp);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@Validated @RequestBody LoginRequest req) {
        try {
            String token = userService.login(req);
            return ResponseEntity.ok(Map.of(
                "token", token,
                "type", "Bearer"
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @GetMapping("/me")
    public ResponseEntity<?> me() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        
        // ✅ FIX: Better null checking
        if (auth == null || !auth.isAuthenticated() || auth.getName() == null) {
            return ResponseEntity.status(401).body(Map.of("error", "Unauthenticated"));
        }
        
        String email = auth.getName();
        
        // ✅ FIX: Handle anonymous authentication
        if ("anonymousUser".equals(email)) {
            return ResponseEntity.status(401).body(Map.of("error", "Unauthenticated"));
        }
        
        var userOpt = userRepository.findByEmail(email);
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(404).body(Map.of("error", "User not found"));
        }
        User u = userOpt.get();
        UserResponse resp = new UserResponse();
        resp.setUserId(u.getUserId());
        resp.setName(u.getFullName());
        resp.setEmail(u.getEmail());
        return ResponseEntity.ok(resp);
    }
}