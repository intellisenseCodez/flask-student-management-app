-- Create database
CREATE DATABASE IF NOT EXISTS student_db;

-- Create user if not exists
CREATE USER IF NOT EXISTS 'testuser'@'%' IDENTIFIED BY 'testpassword';

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON student_db.* TO 'testuser'@'%';

-- Apply the changes
FLUSH PRIVILEGES;
