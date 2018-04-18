CREATE TABLE users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_role TEXT NOT NULL DEFAULT 'user',
  user_name TEXT NOT NULL UNIQUE,
  user_pass TEXT NOT NULL,
  user_fullname TEXT NOT NULL DEFAULT '<blank>',
  user_phone TEXT NOT NULL DEFAULT '<blank>',
  user_email TEXT NOT NULL DEFAULT '<blank>'
);

CREATE TABLE accts (
  acct_id TEXT NOT NULL PRIMARY KEY,
  acct_user INTEGER NOT NULL,
  acct_balance NUMERIC NOT NULL DEFAULT 0.00,
  FOREIGN KEY (acct_user) REFERENCES users(user_id)
);

CREATE TABLE xacts (
  xact_id INTEGER PRIMARY KEY AUTOINCREMENT,
  xact_acct TEXT NOT NULL,
  xact_amount INTEGER NOT NULL DEFAULT 0.00,
  xact_memo TEXT NOT NULL DEFAULT '',
  xact_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (xact_acct) REFERENCES accts(acct_id)
);

