CREATE DATABASE IF NOT EXISTS mouseTracker;
USE mouseTracker;

CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE coordinates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36),
    x_coordinate DOUBLE,
    y_coordinate DOUBLE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36),
    image_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_user ON coordinates (user_id);
CREATE INDEX idx_user_images ON images (user_id);
