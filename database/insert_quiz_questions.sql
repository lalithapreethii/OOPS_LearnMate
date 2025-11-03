-- ========================================
-- BULK INSERT QUIZ QUESTIONS
-- 30 Questions Per Subject (10 Easy, 10 Medium, 10 Hard)
-- ========================================

USE knowwhereyoulack;

-- Get topic IDs first
-- SELECT topic_id, topic_name FROM topics;

-- ========================================
-- OBJECT-ORIENTED PROGRAMMING (OOP)
-- Assuming topic_id = 1 (adjust based on your database)
-- ========================================

-- EASY (10 questions)
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation, is_active) VALUES
(1, 'What does OOP stand for?', 'MCQ', 'EASY', 'Object-Oriented Programming', 'OOP is a programming paradigm based on objects and classes', TRUE),
(1, 'Which keyword is used to create a class in Java?', 'MCQ', 'EASY', 'class', 'The class keyword defines a new class in Java', TRUE),
(1, 'What is an object?', 'MCQ', 'EASY', 'Instance of a class', 'An object is a runtime entity created from a class blueprint', TRUE),
(1, 'Which access modifier makes members visible only inside the class?', 'MCQ', 'EASY', 'private', 'Private members cannot be accessed from outside the class', TRUE),
(1, 'What is inheritance?', 'MCQ', 'EASY', 'A class deriving properties from another class', 'Inheritance allows code reusability through parent-child relationship', TRUE),
(1, 'Which symbol is used to access class members in Java?', 'MCQ', 'EASY', '.', 'The dot operator accesses fields and methods of an object', TRUE),
(1, 'What is a constructor?', 'MCQ', 'EASY', 'Special method called when object is created', 'Constructors initialize objects and have the same name as the class', TRUE),
(1, 'Can a class have multiple constructors in Java?', 'MCQ', 'EASY', 'Yes', 'Constructor overloading allows multiple constructors with different parameters', TRUE),
(1, 'What is method overloading?', 'MCQ', 'EASY', 'Same method name with different parameters', 'Method overloading is compile-time polymorphism', TRUE),
(1, 'Which keyword is used for inheritance in Java?', 'MCQ', 'EASY', 'extends', 'The extends keyword establishes inheritance relationship', TRUE);

-- MEDIUM (10 questions)
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation, is_active) VALUES
(1, 'Which concept allows using the same function name with different implementations?', 'MCQ', 'MEDIUM', 'Polymorphism', 'Polymorphism means many forms - one interface, multiple implementations', TRUE),
(1, 'What is encapsulation?', 'MCQ', 'MEDIUM', 'Hiding internal details and providing public interface', 'Encapsulation bundles data and methods that operate on that data', TRUE),
(1, 'What is abstraction in OOP?', 'MCQ', 'MEDIUM', 'Hiding implementation details and showing only functionality', 'Abstraction focuses on what an object does rather than how', TRUE),
(1, 'Which keyword prevents method overriding in Java?', 'MCQ', 'MEDIUM', 'final', 'Final methods cannot be overridden in subclasses', TRUE),
(1, 'What is the super keyword used for?', 'MCQ', 'MEDIUM', 'Accessing parent class members', 'Super refers to immediate parent class object', TRUE),
(1, 'Can abstract classes be instantiated?', 'MCQ', 'MEDIUM', 'No', 'Abstract classes are incomplete and cannot create objects directly', TRUE),
(1, 'What is method overriding?', 'MCQ', 'MEDIUM', 'Redefining parent class method in child class', 'Method overriding is runtime polymorphism', TRUE),
(1, 'Which OOPS concept supports code reusability?', 'MCQ', 'MEDIUM', 'Inheritance', 'Inheritance allows child classes to reuse parent class code', TRUE),
(1, 'What is the purpose of getters and setters?', 'MCQ', 'MEDIUM', 'Accessing private members safely with validation', 'Getters and setters provide controlled access to private fields', TRUE),
(1, 'What is the difference between interface and abstract class?', 'MCQ', 'MEDIUM', 'Interface has only abstract methods by default', 'Interfaces define contracts, abstract classes can have implementation', TRUE);

-- HARD (10 questions)
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation, is_active) VALUES
(1, 'What is dynamic polymorphism?', 'MCQ', 'HARD', 'Runtime polymorphism through method overriding', 'Dynamic binding occurs at runtime using virtual functions', TRUE),
(1, 'Which SOLID principle states a class should have only one reason to change?', 'MCQ', 'HARD', 'Single Responsibility Principle', 'SRP promotes high cohesion and low coupling', TRUE),
(1, 'What is the Liskov Substitution Principle?', 'MCQ', 'HARD', 'Objects of superclass should be replaceable with subclass objects', 'LSP ensures derived classes extend base classes without changing behavior', TRUE),
(1, 'What does composition over inheritance mean?', 'MCQ', 'HARD', 'Favor object composition over class inheritance', 'Composition provides more flexibility than rigid inheritance hierarchies', TRUE),
(1, 'What is the diamond problem in multiple inheritance?', 'MCQ', 'HARD', 'Ambiguity in method resolution from multiple parent classes', 'Diamond problem occurs when a class inherits from two classes with same method', TRUE),
(1, 'What is covariant return type?', 'MCQ', 'HARD', 'Overriding method can return subclass of return type', 'Covariant return types provide more specific return types in overriding', TRUE),
(1, 'What is RTTI?', 'MCQ', 'HARD', 'Runtime Type Identification', 'RTTI allows determining object type during program execution', TRUE),
(1, 'What is the difference between association and aggregation?', 'MCQ', 'HARD', 'Aggregation implies ownership while association does not', 'Aggregation is has-a relationship with lifecycle dependency', TRUE),
(1, 'What is the purpose of protected access modifier?', 'MCQ', 'HARD', 'Accessible in subclass but not outside package', 'Protected provides inheritance-based access control', TRUE),
(1, 'What is interface segregation principle?', 'MCQ', 'HARD', 'Clients should not depend on interfaces they do not use', 'ISP prevents fat interfaces and promotes specific, focused interfaces', TRUE);

-- Add options for each question
-- (This would be in question_options table if you have MCQ options)

-- ========================================
-- DATA STRUCTURES & ALGORITHMS (DSA)
-- Assuming topic_id = 2
-- ========================================

-- EASY (10 questions)
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation, is_active) VALUES
(2, 'What is an array?', 'MCQ', 'EASY', 'Contiguous memory locations storing same data type', 'Arrays provide indexed access to elements', TRUE),
(2, 'What is the time complexity of accessing an array element by index?', 'MCQ', 'EASY', 'O(1)', 'Array indexing is constant time operation', TRUE),
(2, 'What is a linked list?', 'MCQ', 'EASY', 'Linear data structure with nodes containing data and pointer', 'Linked lists allow dynamic memory allocation', TRUE),
(2, 'What is a stack?', 'MCQ', 'EASY', 'LIFO data structure', 'Stack follows Last In First Out principle', TRUE),
(2, 'What is a queue?', 'MCQ', 'EASY', 'FIFO data structure', 'Queue follows First In First Out principle', TRUE),
(2, 'Which operation is used to add element to stack?', 'MCQ', 'EASY', 'push', 'Push adds element to top of stack', TRUE),
(2, 'Which operation removes element from queue?', 'MCQ', 'EASY', 'dequeue', 'Dequeue removes element from front of queue', TRUE),
(2, 'What is binary search?', 'MCQ', 'EASY', 'Searching in sorted array by dividing in half', 'Binary search has O(log n) complexity', TRUE),
(2, 'What is the advantage of linked list over array?', 'MCQ', 'EASY', 'Dynamic size', 'Linked lists can grow and shrink dynamically', TRUE),
(2, 'What is a tree?', 'MCQ', 'EASY', 'Hierarchical data structure with nodes', 'Trees have parent-child relationships', TRUE);

-- MEDIUM (10 questions)
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation, is_active) VALUES
(2, 'What is the time complexity of binary search?', 'MCQ', 'MEDIUM', 'O(log n)', 'Binary search halves the search space each iteration', TRUE),
(2, 'What is a hash table?', 'MCQ', 'MEDIUM', 'Data structure using hash function for key-value mapping', 'Hash tables provide O(1) average case lookup', TRUE),
(2, 'What is a binary tree?', 'MCQ', 'MEDIUM', 'Tree where each node has at most 2 children', 'Binary trees are fundamental in many algorithms', TRUE),
(2, 'What is the difference between stack and queue?', 'MCQ', 'MEDIUM', 'Stack is LIFO, Queue is FIFO', 'Different order of element removal', TRUE),
(2, 'What is recursion?', 'MCQ', 'MEDIUM', 'Function calling itself', 'Recursion breaks problems into smaller subproblems', TRUE),
(2, 'What is dynamic programming?', 'MCQ', 'MEDIUM', 'Optimization technique storing subproblem results', 'DP avoids redundant calculations through memoization', TRUE),
(2, 'What is a graph?', 'MCQ', 'MEDIUM', 'Non-linear data structure with vertices and edges', 'Graphs represent relationships between objects', TRUE),
(2, 'What is BFS?', 'MCQ', 'MEDIUM', 'Breadth First Search exploring level by level', 'BFS uses queue and finds shortest path in unweighted graphs', TRUE),
(2, 'What is DFS?', 'MCQ', 'MEDIUM', 'Depth First Search exploring as far as possible', 'DFS uses stack or recursion', TRUE),
(2, 'What is the time complexity of quicksort average case?', 'MCQ', 'MEDIUM', 'O(n log n)', 'Quicksort is efficient divide-and-conquer algorithm', TRUE);

-- HARD (10 questions)
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation, is_active) VALUES
(2, 'What is the time complexity of finding LCA in binary tree?', 'MCQ', 'HARD', 'O(n)', 'Lowest Common Ancestor requires traversing tree', TRUE),
(2, 'What is AVL tree?', 'MCQ', 'HARD', 'Self-balancing binary search tree', 'AVL maintains height balance factor of -1, 0, or 1', TRUE),
(2, 'What is the space complexity of merge sort?', 'MCQ', 'HARD', 'O(n)', 'Merge sort requires auxiliary array for merging', TRUE),
(2, 'What is Dijkstra algorithm used for?', 'MCQ', 'HARD', 'Finding shortest path in weighted graph', 'Dijkstra uses greedy approach with priority queue', TRUE),
(2, 'What is topological sort?', 'MCQ', 'HARD', 'Linear ordering of vertices in DAG', 'Topological sort used in task scheduling', TRUE),
(2, 'What is the difference between Dijkstra and Bellman-Ford?', 'MCQ', 'HARD', 'Bellman-Ford handles negative weights', 'Dijkstra fails with negative edge weights', TRUE),
(2, 'What is segment tree used for?', 'MCQ', 'HARD', 'Range queries and updates in O(log n)', 'Segment trees efficiently handle range sum/min/max queries', TRUE),
(2, 'What is trie?', 'MCQ', 'HARD', 'Tree for storing strings efficiently', 'Trie enables fast prefix-based searches', TRUE),
(2, 'What is union-find data structure?', 'MCQ', 'HARD', 'Disjoint set for connectivity queries', 'Union-Find used in Kruskal MST algorithm', TRUE),
(2, 'What is the time complexity of heap insert?', 'MCQ', 'HARD', 'O(log n)', 'Heap maintains complete binary tree property', TRUE);

-- ========================================
-- PHYSICS
-- Assuming topic_id = 3
-- ========================================

-- EASY (10 questions)
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation, is_active) VALUES
(3, 'What is the SI unit of force?', 'MCQ', 'EASY', 'Newton', 'Named after Isaac Newton', TRUE),
(3, 'What is the formula for speed?', 'MCQ', 'EASY', 'Distance/Time', 'Speed measures how fast object moves', TRUE),
(3, 'What is Newton''s first law?', 'MCQ', 'EASY', 'Object at rest stays at rest unless acted upon', 'Law of inertia', TRUE),
(3, 'What is the SI unit of energy?', 'MCQ', 'EASY', 'Joule', 'Energy can be converted but not destroyed', TRUE),
(3, 'What is velocity?', 'MCQ', 'EASY', 'Speed with direction', 'Velocity is a vector quantity', TRUE),
(3, 'What is acceleration?', 'MCQ', 'EASY', 'Rate of change of velocity', 'Acceleration measured in m/s²', TRUE),
(3, 'What is gravity?', 'MCQ', 'EASY', 'Force that attracts objects toward Earth', 'Gravity gives weight to objects', TRUE),
(3, 'What is the speed of light?', 'MCQ', 'EASY', '3 × 10^8 m/s', 'Light travels fastest in vacuum', TRUE),
(3, 'What is kinetic energy?', 'MCQ', 'EASY', 'Energy of motion', 'KE = 1/2 mv²', TRUE),
(3, 'What is potential energy?', 'MCQ', 'EASY', 'Stored energy due to position', 'PE = mgh for gravitational potential', TRUE);

-- MEDIUM (10 questions)
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation, is_active) VALUES
(3, 'What is Newton''s second law formula?', 'MCQ', 'MEDIUM', 'F = ma', 'Force equals mass times acceleration', TRUE),
(3, 'What is momentum?', 'MCQ', 'MEDIUM', 'Mass times velocity', 'Momentum is conserved in collisions', TRUE),
(3, 'What is work in physics?', 'MCQ', 'MEDIUM', 'Force times displacement', 'W = F × d × cos(θ)', TRUE),
(3, 'What is power?', 'MCQ', 'MEDIUM', 'Rate of doing work', 'P = W/t measured in watts', TRUE),
(3, 'What is Ohm''s law?', 'MCQ', 'MEDIUM', 'V = IR', 'Voltage equals current times resistance', TRUE),
(3, 'What is frequency?', 'MCQ', 'MEDIUM', 'Number of waves per second', 'Measured in Hertz (Hz)', TRUE),
(3, 'What is wavelength?', 'MCQ', 'MEDIUM', 'Distance between wave crests', 'Related to frequency by wave equation', TRUE),
(3, 'What is Hooke''s law?', 'MCQ', 'MEDIUM', 'F = -kx', 'Force in spring proportional to displacement', TRUE),
(3, 'What is centripetal force?', 'MCQ', 'MEDIUM', 'Force toward center of circular motion', 'Keeps object moving in circle', TRUE),
(3, 'What is conservation of energy?', 'MCQ', 'MEDIUM', 'Energy cannot be created or destroyed', 'Total energy remains constant', TRUE);

-- HARD (10 questions)
INSERT INTO questions (topic_id, question_text, question_type, difficulty_level, correct_answer, explanation, is_active) VALUES
(3, 'What is the Heisenberg Uncertainty Principle?', 'MCQ', 'HARD', 'Cannot know position and momentum simultaneously', 'Fundamental limit in quantum mechanics', TRUE),
(3, 'What is Maxwell''s equation describe?', 'MCQ', 'HARD', 'Electromagnetic field behavior', 'Four equations unify electricity and magnetism', TRUE),
(3, 'What is Schrödinger equation?', 'MCQ', 'HARD', 'Describes quantum state evolution', 'Foundation of quantum mechanics', TRUE),
(3, 'What is special relativity key postulate?', 'MCQ', 'HARD', 'Speed of light constant in all frames', 'Leads to time dilation and length contraction', TRUE),
(3, 'What is E = mc²?', 'MCQ', 'HARD', 'Energy-mass equivalence', 'Matter can be converted to energy', TRUE),
(3, 'What is entropy?', 'MCQ', 'HARD', 'Measure of disorder in system', 'Second law of thermodynamics', TRUE),
(3, 'What is the Doppler effect?', 'MCQ', 'HARD', 'Frequency change due to relative motion', 'Explains redshift in astronomy', TRUE),
(3, 'What is black body radiation?', 'MCQ', 'HARD', 'Electromagnetic radiation from ideal absorber', 'Led to quantum theory development', TRUE),
(3, 'What is the Pauli exclusion principle?', 'MCQ', 'HARD', 'No two fermions can occupy same quantum state', 'Explains electron shell structure', TRUE),
(3, 'What is superconductivity?', 'MCQ', 'HARD', 'Zero electrical resistance below critical temperature', 'Quantum mechanical phenomenon', TRUE);

-- ========================================
-- Continue for remaining subjects:
-- - Chemistry (topic_id = 4)
-- - Operating Systems (topic_id = 5)
-- - Mathematics (topic_id = 6)
-- - Biology (topic_id = 7)
-- - AI/ML Basics (topic_id = 8)
-- ========================================

-- Verify insertion
SELECT 
    t.topic_name,
    q.difficulty_level,
    COUNT(*) as question_count
FROM questions q
JOIN topics t ON q.topic_id = t.topic_id
WHERE q.is_active = TRUE
GROUP BY t.topic_name, q.difficulty_level
ORDER BY t.topic_name, q.difficulty_level;

-- Expected result: Each topic should have 10 EASY, 10 MEDIUM, 10 HARD = 30 total
