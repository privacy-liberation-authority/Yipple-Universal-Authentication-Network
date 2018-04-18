# Build 3
## Overview
Our users have realised that the Yipple Universal Authentication Network is severely limited by the 1MB blocksize, with transfer times in excess of hours. Hence, we need you to reimplement our transaction processing system in an efficient and secure manner. Although we are advertising a blockchain based system, it is imperative we have a working system in place by next week, before the Syber Blockchain Credit Union.

You are required to carry out the following tasks:
1. Implement SQL queries for the `Acct` (Account) model.
2. Implement method stubs for the `Xact` (Transaction) model.
3. Implement the `do_transfer(src, dst, amount, memo)` function.

The provided code does not use SQLAlchemy so that you're exposed to writing SQL yourself. 
After completing the required tasks, research SQLAlchemy and consider how you might convert the web app to use it instead.
It can greatly simplify working with database models!

## What you have currently.

A functional KomradeBank web app is provided for you. You should not need to edit or modify any routes, templates or forms. Each area that you need to complete is clearly identified with a `TODO` comment explaining what is required.

The SQL database schema is provided below. You should NOT modify or add to this.

```sql
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
```

## Getting Started

First you should install the web app dependencies with the following commands,

1. `virtualenv venv`
2. `source ./venv/bin/activate`
3. `pip install -r requirements.txt`

Then you can run the web app with `./run.py` or `python3 run.py` command in the repo root directory.

If the database doesn't exist, it will be created automatically. The database can be reset by executing with `./run.py -drop`

> You will not be able to run the web app until you've successfully implemented the methods for the `Acct` and `Xact` database models.


## Running Tests

To run tests, run the `./test.py` or `python3 test.py` command in the repo root directory.

The database will be reset automatically to it's initial default state for each test.

NOTE: You may require `chromedriver` in order for selenium to run the tests successfully. Download links for each platform can be found at:

https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver

## Required Tasks
### 1. Complete `Acct` model methods (models.py)

The `Acct` model is fully implemented for you already, except for the SQL query strings as shown in the example below.
Replace the marked `TODO` strings with valid SQL queries to perform the desired action.

> The Acct.by_id(acct_id) method with stubbed out SQL query string.

```python
@staticmethod
def by_id(acct_id):
    row = db.get('-- TODO: write SQL query to return a single row for a specific account id', [acct_id])
    if row is None:
        return None
    return Acct._from_row(row)
```

There are 4 SQL strings in total to complete the following methods,
- `Acct.new(user_id)`
- `Acct.by_id(acct_id)`
- `Acct.by_user_id(user_id)`
- `Acct.by_filter(filter)`

Feel free to inspect the `User` model as a guide for how these queries work.


### 2. Complete `Xact` model methods (models.py)

A skeleton `Xact` model is provided without implementation. Rather then just writing the SQL query strings, now you're also required to complete the python implementation of the defined methods.

> The Xact.by_id(xact_id) method skeleton that needs implementing. 

```python
@staticmethod
def by_id(xact_id):

    # TODO: Implement method to return the transaction for a given id.

    # Returns Xact object
    return None
```

There are 4 model methods in total to implement,
- `Xact.new(acct_id, memo, amount)`
- `Xact.by_id(xact_id)`
- `Xact.by_acct_id(acct_id)`
- `Xact.by_filter(filter)`

Use the `User` and `Acct` models as a guide for your implementation.

### 3. Complete `do_transfer(src, dst, amount, memo)` function (models.py)

Follow the instructions provided in the function comments to implement the logic for transferring funds from one account to another.

The necessary information is provided to the function by the existing transfer route/form, but it is your responsibility to check the input and ensure it's a valid transfer. Specifically,
- Both accounts should exist and not be the same.
- Source account should have sufficient funds to perform transfer.
- Amount should be greater than zero.

There are 4 SQL queries also required to update the database to represent a transfer. 

> After successfully completing these tasks you should be able to login and view a user's transactions, their account balance and use the provided transfer route/form in the KomradeBank wep app to perform fund transfers between user accounts.
