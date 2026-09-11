CREATE DATABASE IF NOT EXISTS mydb;

USE mydb;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    password_hash CHAR(128) NOT NULL
);

INSERT INTO users (username, password_hash) VALUES
('AliceUser', SHA2('password', 512)),
('BobUser', SHA2('password', 512));