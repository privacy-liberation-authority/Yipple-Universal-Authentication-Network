import os
import json
import bcrypt
import uuid

from .db import getDB, queryDB, insertDB

def registerUser(username, password):
    isSuccess = False

    # Check input lengths
    if len(username) == 0 or len(password) == 0:
        return (isSuccess, 'Invalid username or password length')

    # Check username uniqueness
    res = queryDB('SELECT * FROM users WHERE username = ?', [username], one=True)
    if res is not None:
        # User already exists inside the database
        return (isSuccess, 'The supplied username is already in use')
    else:
        # Registration successful
        insertDB('INSERT INTO users (username, passhash) values (?, ?)', (username, password))
        isSuccess = True
    return (isSuccess, 'Registration successful')

# Returns tuple of (success, session)
# Session is the username in this case.
def validateUser(username, password):
    isSuccess = False

    if len(username) == 0 or len(password) == 0:
        return (isSuccess, None)

    res = queryDB('SELECT * FROM users WHERE username = ?', [username], one=True)

    if res is not None:
        if res[2] == password:
            # Login succeeded
            isSuccess = True
            return (isSuccess, username)
        return (isSuccess, username)

    return (isSuccess, None)

