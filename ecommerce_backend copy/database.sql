CREATE DATABASE learning_platform;
USE learning_platform;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  password VARCHAR(100)
);

CREATE TABLE courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200),
  description TEXT
);

CREATE TABLE enrollments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  course_id INT,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE progress (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  course_id INT,
  progress_percent INT,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE quizzes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  course_id INT,
  question TEXT,
  answer VARCHAR(255),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

INSERT INTO courses (title, description)
VALUES 
('Python Basics', 'Learn Python fundamentals: variables, loops, functions'),
('Web Development', 'Build websites using HTML, CSS, and JavaScript'),
('Data Science 101', 'Introduction to data science concepts and tools');

INSERT INTO users (name, email, password)
VALUES 
('Preetam', 'preetam@example.com', '12345'),
('Aarav', 'aarav@example.com', 'password'),
('Meera', 'meera@example.com', 'test123');
