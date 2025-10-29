-- KnowWhereYouLack Database Schema
-- MySQL 8.0+

DROP DATABASE IF EXISTS knowwhereyoulack;
CREATE DATABASE knowwhereyoulack;
USE knowwhereyoulack;

-- =====================================================
-- 1. USERS TABLE
-- =====================================================
CREATE TABLE users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('STUDENT', 'TEACHER', 'ADMIN') DEFAULT 'STUDENT',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 2. SUBJECTS TABLE
-- =====================================================
CREATE TABLE subjects (
    subject_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    subject_code VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_subject_code (subject_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 3. TOPICS TABLE
-- =====================================================
CREATE TABLE topics (
    topic_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    subject_id BIGINT NOT NULL,
    topic_name VARCHAR(150) NOT NULL,
    topic_order INT DEFAULT 0,
    difficulty_level ENUM('EASY', 'MEDIUM', 'HARD') DEFAULT 'MEDIUM',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    INDEX idx_subject_id (subject_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 4. QUESTIONS TABLE
-- =====================================================
CREATE TABLE questions (
    question_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    topic_id BIGINT NOT NULL,
    question_text TEXT NOT NULL,
    question_type ENUM('MCQ', 'TRUE_FALSE', 'SHORT_ANSWER') DEFAULT 'MCQ',
    difficulty_level ENUM('EASY', 'MEDIUM', 'HARD') DEFAULT 'MEDIUM',
    correct_answer VARCHAR(500) NOT NULL,
    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE,
    INDEX idx_topic_id (topic_id),
    INDEX idx_difficulty (difficulty_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 5. QUESTION OPTIONS TABLE (for MCQs)
-- =====================================================
CREATE TABLE question_options (
    option_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    question_id BIGINT NOT NULL,
    option_text VARCHAR(500) NOT NULL,
    option_label VARCHAR(10) NOT NULL, -- A, B, C, D
    is_correct BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
    INDEX idx_question_id (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 6. QUIZ ATTEMPTS TABLE
-- =====================================================
CREATE TABLE quiz_attempts (
    attempt_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    topic_id BIGINT NOT NULL,
    total_questions INT NOT NULL,
    correct_answers INT NOT NULL,
    score_percentage DECIMAL(5,2) NOT NULL,
    time_taken_seconds INT NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_topic_id (topic_id),
    INDEX idx_completed_at (completed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 7. QUIZ RESPONSES TABLE (individual answers)
-- =====================================================
CREATE TABLE quiz_responses (
    response_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    attempt_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    user_answer VARCHAR(500),
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INT,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (attempt_id) REFERENCES quiz_attempts(attempt_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
    INDEX idx_attempt_id (attempt_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 8. WEAKNESS ANALYSIS TABLE (ML predictions)
-- =====================================================
CREATE TABLE weakness_analysis (
    analysis_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    topic_id BIGINT NOT NULL,
    strength_level ENUM('WEAK', 'MODERATE', 'STRONG') NOT NULL,
    confidence_score DECIMAL(5,4) NOT NULL, -- 0.0000 to 1.0000
    avg_score DECIMAL(5,2),
    total_attempts INT DEFAULT 0,
    last_attempt_date TIMESTAMP,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_topic (user_id, topic_id),
    INDEX idx_user_id (user_id),
    INDEX idx_strength_level (strength_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 9. LEARNING RESOURCES TABLE
-- =====================================================
CREATE TABLE learning_resources (
    resource_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    topic_id BIGINT NOT NULL,
    resource_type ENUM('VIDEO', 'ARTICLE', 'PRACTICE', 'BOOK') NOT NULL,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,
    description TEXT,
    difficulty_level ENUM('BEGINNER', 'INTERMEDIATE', 'ADVANCED') DEFAULT 'INTERMEDIATE',
    duration_minutes INT,
    relevance_score DECIMAL(3,2) DEFAULT 0.80, -- 0.00 to 1.00
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE,
    INDEX idx_topic_id (topic_id),
    INDEX idx_resource_type (resource_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 10. RECOMMENDATIONS TABLE (personalized)
-- =====================================================
CREATE TABLE recommendations (
    recommendation_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    resource_id BIGINT NOT NULL,
    reason VARCHAR(255), -- "Based on your weakness in Loops"
    recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_viewed BOOLEAN DEFAULT FALSE,
    is_completed BOOLEAN DEFAULT FALSE,
    feedback_rating INT, -- 1-5 stars
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (resource_id) REFERENCES learning_resources(resource_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_recommended_at (recommended_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 11. CHAT HISTORY TABLE (chatbot conversations)
-- =====================================================
CREATE TABLE chat_history (
    chat_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    message TEXT NOT NULL,
    sender ENUM('USER', 'BOT') NOT NULL,
    context_topics VARCHAR(255), -- JSON array of topic_ids
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 12. STUDY PLANS TABLE
-- =====================================================
CREATE TABLE study_plans (
    plan_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    goal_description TEXT,
    status ENUM('ACTIVE', 'COMPLETED', 'ABANDONED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 13. STUDY PLAN TASKS TABLE
-- =====================================================
CREATE TABLE study_plan_tasks (
    task_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    plan_id BIGINT NOT NULL,
    topic_id BIGINT NOT NULL,
    task_description VARCHAR(255) NOT NULL,
    scheduled_date DATE NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP NULL,
    
    FOREIGN KEY (plan_id) REFERENCES study_plans(plan_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE,
    INDEX idx_plan_id (plan_id),
    INDEX idx_scheduled_date (scheduled_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert sample subjects
INSERT INTO subjects (subject_name, subject_code, description) VALUES
('Data Structures', 'CS201', 'Fundamental data structures and algorithms'),
('Database Management', 'CS301', 'Relational databases and SQL'),
('Machine Learning', 'CS401', 'Introduction to ML concepts and algorithms');

-- Insert sample topics for Data Structures
INSERT INTO topics (subject_id, topic_name, topic_order, difficulty_level, description) VALUES
(1, 'Arrays and Strings', 1, 'EASY', 'Basic array operations and string manipulation'),
(1, 'Linked Lists', 2, 'MEDIUM', 'Singly, doubly, and circular linked lists'),
(1, 'Stacks and Queues', 3, 'MEDIUM', 'Stack and queue implementations'),
(1, 'Trees', 4, 'HARD', 'Binary trees, BST, AVL trees'),
(1, 'Graphs', 5, 'HARD', 'Graph representations and algorithms');

-- Insert sample user (password: demo123 - hashed with BCrypt)
INSERT INTO users (username, email, password_hash, full_name, role) VALUES
('demo_student', 'demo@student.com', '$2a$10$XQxZ8H9KO6P1YF3QR5.GCOyJ8Z7V3K9L6M4N2P0Q8R7S6T5U4V3W2X', 'Demo Student', 'STUDENT'),
('demo_teacher', 'demo@teacher.com', '$2a$10$XQxZ8H9KO6P1YF3QR5.GCOyJ8Z7V3K9L6M4N2P0Q8R7S6T5U4V3W2X', 'Demo Teacher', 'TEACHER');

-- Insert sample questions for "Arrays and Strings"
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation) VALUES
(1, 'What is the time complexity of accessing an element in an array by index?', 'MCQ', 'EASY', 'A', 'Array elements are stored contiguously in memory, allowing direct access in O(1) time.'),
(1, 'Which operation is most efficient on an array?', 'MCQ', 'MEDIUM', 'B', 'Random access is O(1) while insertion/deletion can be O(n).');

-- Insert options for first question
INSERT INTO question_options (question_id, option_text, option_label, is_correct) VALUES
(1, 'O(1)', 'A', TRUE),
(1, 'O(n)', 'B', FALSE),
(1, 'O(log n)', 'C', FALSE),
(1, 'O(n^2)', 'D', FALSE);

-- Insert options for second question
INSERT INTO question_options (question_id, option_text, option_label, is_correct) VALUES
(2, 'Insertion at beginning', 'A', FALSE),
(2, 'Random access', 'B', TRUE),
(2, 'Deletion at middle', 'C', FALSE),
(2, 'Resizing', 'D', FALSE);

-- Insert sample learning resources
INSERT INTO learning_resources (topic_id, resource_type, title, url, description, difficulty_level, duration_minutes) VALUES
(1, 'VIDEO', 'Arrays Explained - CS50', 'https://www.youtube.com/watch?v=example1', 'Introduction to arrays with examples', 'BEGINNER', 15),
(1, 'ARTICLE', 'Array Operations in Java', 'https://www.geeksforgeeks.org/arrays-in-java/', 'Comprehensive guide to array operations', 'INTERMEDIATE', 20),
(2, 'VIDEO', 'Linked Lists Tutorial', 'https://www.youtube.com/watch?v=example2', 'Visual guide to linked lists', 'INTERMEDIATE', 25),
(3, 'PRACTICE', 'Stack Problems - LeetCode', 'https://leetcode.com/tag/stack/', 'Practice problems on stacks', 'INTERMEDIATE', 60);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- View: User performance summary
CREATE VIEW user_performance_summary AS
SELECT 
    u.user_id,
    u.username,
    u.full_name,
    COUNT(DISTINCT qa.attempt_id) AS total_attempts,
    ROUND(AVG(qa.score_percentage), 2) AS avg_score,
    COUNT(DISTINCT CASE WHEN wa.strength_level = 'WEAK' THEN wa.topic_id END) AS weak_topics_count,
    COUNT(DISTINCT CASE WHEN wa.strength_level = 'MODERATE' THEN wa.topic_id END) AS moderate_topics_count,
    COUNT(DISTINCT CASE WHEN wa.strength_level = 'STRONG' THEN wa.topic_id END) AS strong_topics_count
FROM users u
LEFT JOIN quiz_attempts qa ON u.user_id = qa.user_id
LEFT JOIN weakness_analysis wa ON u.user_id = wa.user_id
GROUP BY u.user_id, u.username, u.full_name;

-- View: Topic difficulty analysis
CREATE VIEW topic_difficulty_analysis AS
SELECT 
    t.topic_id,
    t.topic_name,
    s.subject_name,
    COUNT(qa.attempt_id) AS total_attempts,
    ROUND(AVG(qa.score_percentage), 2) AS avg_score,
    COUNT(CASE WHEN wa.strength_level = 'WEAK' THEN 1 END) AS students_struggling,
    COUNT(CASE WHEN wa.strength_level = 'STRONG' THEN 1 END) AS students_excelling
FROM topics t
JOIN subjects s ON t.subject_id = s.subject_id
LEFT JOIN quiz_attempts qa ON t.topic_id = qa.topic_id
LEFT JOIN weakness_analysis wa ON t.topic_id = wa.topic_id
GROUP BY t.topic_id, t.topic_name, s.subject_name;

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Composite indexes for common queries
CREATE INDEX idx_user_topic_analysis ON weakness_analysis(user_id, topic_id, strength_level);
CREATE INDEX idx_attempt_user_date ON quiz_attempts(user_id, completed_at);
CREATE INDEX idx_resource_topic_type ON learning_resources(topic_id, resource_type, is_active);

-- =====================================================
-- STORED PROCEDURES
-- =====================================================

DELIMITER //

-- Get user's weak topics with recommendations
CREATE PROCEDURE GetUserWeakTopicsWithRecommendations(IN p_user_id BIGINT)
BEGIN
    SELECT 
        t.topic_id,
        t.topic_name,
        s.subject_name,
        wa.strength_level,
        wa.confidence_score,
        wa.avg_score,
        COUNT(lr.resource_id) AS available_resources
    FROM weakness_analysis wa
    JOIN topics t ON wa.topic_id = t.topic_id
    JOIN subjects s ON t.subject_id = s.subject_id
    LEFT JOIN learning_resources lr ON t.topic_id = lr.topic_id AND lr.is_active = TRUE
    WHERE wa.user_id = p_user_id AND wa.strength_level = 'WEAK'
    GROUP BY t.topic_id, t.topic_name, s.subject_name, wa.strength_level, wa.confidence_score, wa.avg_score
    ORDER BY wa.avg_score ASC, wa.confidence_score DESC;
END //

-- Calculate and update weakness analysis
CREATE PROCEDURE UpdateWeaknessAnalysis(IN p_user_id BIGINT, IN p_topic_id BIGINT)
BEGIN
    DECLARE v_avg_score DECIMAL(5,2);
    DECLARE v_total_attempts INT;
    DECLARE v_last_attempt TIMESTAMP;
    DECLARE v_strength_level VARCHAR(20);
    
    -- Calculate statistics
    SELECT 
        AVG(score_percentage),
        COUNT(*),
        MAX(completed_at)
    INTO v_avg_score, v_total_attempts, v_last_attempt
    FROM quiz_attempts
    WHERE user_id = p_user_id AND topic_id = p_topic_id;
    
    -- Determine strength level
    IF v_avg_score IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No quiz attempts found';
    ELSEIF v_avg_score < 60 THEN
        SET v_strength_level = 'WEAK';
    ELSEIF v_avg_score < 80 THEN
        SET v_strength_level = 'MODERATE';
    ELSE
        SET v_strength_level = 'STRONG';
    END IF;
    
    -- Insert or update weakness analysis
    INSERT INTO weakness_analysis (
        user_id, topic_id, strength_level, confidence_score, 
        avg_score, total_attempts, last_attempt_date
    )
    VALUES (
        p_user_id, p_topic_id, v_strength_level, 0.85,
        v_avg_score, v_total_attempts, v_last_attempt
    )
    ON DUPLICATE KEY UPDATE
        strength_level = v_strength_level,
        avg_score = v_avg_score,
        total_attempts = v_total_attempts,
        last_attempt_date = v_last_attempt,
        analyzed_at = CURRENT_TIMESTAMP;
END //

DELIMITER ;

-- =====================================================
-- GRANT PERMISSIONS (for application user)
-- =====================================================

-- Create application user
CREATE USER IF NOT EXISTS 'kwyl_app'@'localhost' IDENTIFIED BY 'SecurePassword123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON knowwhereyoulack.* TO 'kwyl_app'@'localhost';
GRANT EXECUTE ON knowwhereyoulack.* TO 'kwyl_app'@'localhost';
FLUSH PRIVILEGES;

SELECT 'Database schema created successfully!' AS STATUS;