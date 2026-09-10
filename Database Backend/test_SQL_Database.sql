-- Create database
CREATE DATABASE mydb;

-- Use the database
USE mydb;

-- Create a table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) UNIQUE NOT NULL
);

SET @input := 'password';


-- Insert sample data
INSERT INTO users (username, password) VALUES
('AliceUser', HASHBYTES('SHA2_512', @input)),
('BobUser', HASHBYTES('SHA2_512', @input));

