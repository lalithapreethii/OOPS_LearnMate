-- ========================================
-- SETUP DATABASE TOPICS FIRST
-- Run this BEFORE insert_quiz_questions.sql
-- ========================================

USE knowwhereyoulack;

-- Clear existing data (OPTIONAL - only if you want fresh start)
-- DELETE FROM questions WHERE question_id > 0;
-- DELETE FROM topics WHERE topic_id > 0;
-- DELETE FROM subjects WHERE subject_id > 0;

-- Insert subjects
INSERT INTO subjects (subject_id, subject_name, subject_code, description) VALUES
(1, 'Computer Science', 'CS', 'Programming and computer science fundamentals'),
(2, 'Science', 'SCI', 'Physics, Chemistry, and Biology'),
(3, 'Mathematics', 'MATH', 'Mathematics and quantitative reasoning')
ON DUPLICATE KEY UPDATE subject_name = VALUES(subject_name);

-- Insert topics matching your frontend
INSERT INTO topics (topic_id, subject_id, topic_name, topic_order, difficulty_level, description) VALUES
(1, 1, 'Object-Oriented Programming', 1, 'MEDIUM', 'Test your knowledge of classes, objects, and inheritance'),
(2, 1, 'Data Structures', 2, 'EASY', 'Explore arrays, linked lists, stacks, and queues'),
(3, 1, 'Algorithms', 3, 'HARD', 'Challenge yourself with sorting and searching algorithms'),
(4, 2, 'Physics', 1, 'MEDIUM', 'From kinematics to quantum mechanics'),
(5, 2, 'Chemistry', 2, 'MEDIUM', 'Explore atoms, molecules, and chemical reactions'),
(6, 1, 'Operating Systems', 4, 'HARD', 'Understand processes, memory, and file systems'),
(7, 3, 'Math', 1, 'MEDIUM', 'Calculus, Algebra, and more'),
(8, 2, 'Biology', 3, 'EASY', 'Explore cells, genetics, and evolution'),
(9, 1, 'AIML Basics', 5, 'HARD', 'Fundamentals of AI and Machine Learning')
ON DUPLICATE KEY UPDATE 
    topic_name = VALUES(topic_name),
    description = VALUES(description);

-- Verify topics
SELECT 
    t.topic_id,
    t.topic_name,
    s.subject_name,
    t.difficulty_level,
    t.description
FROM topics t
JOIN subjects s ON t.subject_id = s.subject_id
ORDER BY t.topic_id;

-- Check how many questions each topic has
SELECT 
    t.topic_id,
    t.topic_name,
    COUNT(q.question_id) AS question_count,
    SUM(CASE WHEN q.difficulty_level = 'EASY' THEN 1 ELSE 0 END) AS easy_count,
    SUM(CASE WHEN q.difficulty_level = 'MEDIUM' THEN 1 ELSE 0 END) AS medium_count,
    SUM(CASE WHEN q.difficulty_level = 'HARD' THEN 1 ELSE 0 END) AS hard_count
FROM topics t
LEFT JOIN questions q ON t.topic_id = q.topic_id
GROUP BY t.topic_id, t.topic_name
ORDER BY t.topic_id;

SELECT 'Database topics setup complete!' AS STATUS;
