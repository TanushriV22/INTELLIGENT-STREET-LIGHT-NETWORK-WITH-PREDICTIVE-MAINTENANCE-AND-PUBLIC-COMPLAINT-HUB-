-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS light;

-- Use the database
USE light;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create complaints table
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create admin user (password is 'admin123')
INSERT INTO users (name, email, password, is_admin, created_at)
VALUES (
    'Admin User',
    'admin@example.com',
    '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', -- SHA-256 hash of 'admin123'
    1,
    NOW()
) ON DUPLICATE KEY UPDATE name = 'Admin User';

-- Create test user (password is 'user123')
INSERT INTO users (name, email, password, is_admin, created_at)
VALUES (
    'Test User',
    'user@example.com',
    '96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e', -- SHA-256 hash of 'user123'
    0,
    NOW()
) ON DUPLICATE KEY UPDATE name = 'Test User';

-- Create some sample complaints
INSERT INTO complaints (user_id, location, description, status, created_at)
SELECT id, 'Main Street, Corner of 5th Avenue', 'Streetlight is flickering at night', 'pending', NOW()
FROM users WHERE email = 'user@example.com' LIMIT 1
ON DUPLICATE KEY UPDATE location = 'Main Street, Corner of 5th Avenue';

INSERT INTO complaints (user_id, location, description, status, created_at)
SELECT id, 'Park Avenue, Near Central Park', 'Streetlight is completely out', 'in_progress', DATE_SUB(NOW(), INTERVAL 2 DAY)
FROM users WHERE email = 'user@example.com' LIMIT 1
ON DUPLICATE KEY UPDATE location = 'Park Avenue, Near Central Park';

INSERT INTO complaints (user_id, location, description, status, created_at)
SELECT id, 'Broadway and 42nd Street', 'Streetlight pole is damaged and leaning', 'resolved', DATE_SUB(NOW(), INTERVAL 5 DAY)
FROM users WHERE email = 'user@example.com' LIMIT 1
ON DUPLICATE KEY UPDATE location = 'Broadway and 42nd Street';
