CREATE TABLE users(
    uid SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    passhash TEXT NOT NULL
);

CREATE TABLE creds(
    uid INTEGER,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    email TEXT NOT NULL,
    phonenum TEXT NOT NULL,
    funds INTEGER
);

INSERT INTO users (uid, username, passhash) VALUES (0, 'admin', 'alice');
INSERT INTO users (uid, username, passhash) VALUES (1, 'Bobby\" DROP TABLES;--', '\" OR \"1\"=\"1\"');
INSERT INTO users (uid, username, passhash) VALUES (2, 'carol', '0xbeefcafebabe');

INSERT INTO creds (uid, name, address, email, phonenum, funds) VALUES ('0', 'Alice Administrator', 'Omnipotent', 'alice@alice.com', '+313 373 8483', 31333337);
INSERT INTO creds (uid, name, address, email, phonenum, funds) VALUES ('1', 'Bob Bandit', 'Nowhere', 'bob@bob.com', '-123 456 7890', 1337);
INSERT INTO creds (uid, name, address, email, phonenum, funds) VALUES ('2', 'Sweet Carolina', 'Californ-eye-ay', 'carol@candle.lite', '+66 666 6666', 42);
