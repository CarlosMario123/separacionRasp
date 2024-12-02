import sqlite3
from flask import g
from app.config import Config

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature TEXT,
            humidity TEXT,
            gas_level TEXT,
            synced INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seat1 INTEGER,
            seat2 INTEGER DEFAULT 0,
            seat3 INTEGER DEFAULT 0,
            seat4 INTEGER DEFAULT 0,
            synced INTEGER DEFAULT 0
        )
    ''')
    db.commit()
