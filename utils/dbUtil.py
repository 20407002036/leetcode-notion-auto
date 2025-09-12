import sqlite3

def dbConnection():
    conn = sqlite3.connect('leet.db')
    return conn