CREATE TABLE users(
	uid SERIAL PRIMARY KEY,
	username TEXT NOT NULL UNIQUE,
	passhash TEXT NOT NULL
);

INSERT INTO users (username, passhash) VALUES ('admin', 'alice');
INSERT INTO users (username, passhash) VALUES ('Bobby\" DROP TABLES;--', '\" OR \"1\"=\"1\"');