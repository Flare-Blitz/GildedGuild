CREATE TABLE IF NOT EXISTS parents (
    parent_id INT PRIMARY KEY AUTO_INCREMENT,
    parent_email VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    parent_id INT,
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password CHAR(128) NOT NULL,
    ELO VARCHAR(10) NOT NULL DEFAULT '1200',
    date_of_birth DATE NOT NULL,
    account_pending BOOLEAN NOT NULL DEFAULT TRUE,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES parents(parent_id)
);
CREATE TABLE IF NOT EXISTS bot (
    bot_id INT PRIMARY KEY AUTO_INCREMENT,
    bot_name VARCHAR(50) NOT NULL UNIQUE,
    bot_description VARCHAR(255) DEFAULT 'A bot to Play against'
);
CREATE TABLE IF NOT EXISTS gamestats (
    gamestats_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    isRanked BOOLEAN NOT NULL DEFAULT FALSE,
    winner_id INT,
    gamedate DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES users(user_id),
	FOREIGN KEY (winner_id) REFERENCES users(user_id)
);
CREATE TABLE IF NOT EXISTS participants (
    participant_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    bot_id INT,
    gamestats_id INT,
    turnspot INT NOT NULL,
    ELOchange INT NOT NULL DEFAULT 0,
    score INT NOT NULL DEFAULT 0,
	FOREIGN KEY (user_id) REFERENCES users(user_id),
	FOREIGN KEY (bot_id) REFERENCES bot(bot_id),
	FOREIGN KEY (gamestats_id) REFERENCES gamestats(gamestats_id)
);

/*
Generic SQL insert statements:

User Setup
    INSERT INTO users (username, email, password, date_of_birth)
    VALUES (usernameVariable, emailVariable, HASHBYTES('SHA2_256', passwordVariable), dateOfBirthVariable);

User Setup with Parent
    INSERT INTO parents (parent_email)
    VALUES (parentEmailVariable);
    INSERT INTO users (parent_id, username, email, password, date_of_birth)
    VALUES (LAST_INSERT_ID(), usernameVariable, emailVariable, HASHBYTES('SHA2_256', passwordVariable), dateOfBirthVariable);

Bot Setup
    INSERT INTO bots (bot_name, bot_description)
    VALUES (botNameVariable, botDescriptionVariable);

GameStats Setup
    INSERT INTO gamestats (user_id, isRanked, winner_id)
    VALUES (userIdVariable, isRankedVariable, winnerIdVariable);

*/
INSERT INTO users (username, email, password, date_of_birth)
VALUES ('alice', 'AliceUser@example.com', SHA2('password', 256), '2000-01-01');

INSERT INTO users (username, email, password, date_of_birth)
VALUES ('bob','BobUser@example.com', SHA2('password', 256), '2000-01-01');

INSERT INTO parents (parent_email)
VALUES ('CarlieParent@example.com');
INSERT INTO users (parent_id, username, email, password, date_of_birth)
VALUES (LAST_INSERT_ID(), 'Charlie', 'CharlieUser@example.com', SHA2( 'password', 256), '2000-01-01');


INSERT INTO users (username, email, password, date_of_birth)
VALUES ('Dave', 'DaveUser@example.com', SHA2('password', 256), '2000-01-01');
INSERT INTO parents (parent_email)
VALUES ('DaveParent@example.com');
INSERT INTO users (parent_id, username, email, password, date_of_birth)
VALUES (LAST_INSERT_ID(), 'Erin', 'ErinUser@example.com', SHA2( 'password', 256), '2018-09-01');

INSERT INTO bot (bot_name, bot_description)
VALUES ('Timmy', 'A beginner bot to play against');

INSERT INTO gamestats (user_id, isRanked, winner_id)
SELECT u1.user_id, FALSE, u2.user_id
FROM users u1 JOIN users u2
WHERE u1.username = 'Alice' AND u2.username = 'Bob';