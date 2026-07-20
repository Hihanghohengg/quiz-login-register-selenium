CREATE DATABASE IF NOT EXISTS quiz_pengupil
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;
USE quiz_pengupil;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(70) NOT NULL,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO users (name, username, email, password) VALUES
('Test User', 'testuser', 'testuser@example.com', '$2y$12$cGjrr7Yc9Kio2utnmVPp6OyMuFceCiOWQ6mTvtcwXUTKaWQbKGH0y');
