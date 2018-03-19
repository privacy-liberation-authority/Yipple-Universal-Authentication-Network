# Database Imports
import sqlite3
from flask import g

DATABASE = 'users.db'

def getDB():
    db = getattr(g, '_database', None)
    if db is None:
        db =  g._database = sqlite3.connect(DATABASE)
    return db

def queryDB(query, args=(), one=False):
    cur = getDB().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insertDB(query, args=(), one=False):
    db = getDB()
    db.execute(query, args)
    db.commit()
