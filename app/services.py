from app.db import get_db

def insert_data(temperature, humidity, gas_level):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO data (temperature, humidity, gas_level) VALUES (?, ?, ?)', 
                   (temperature, humidity, gas_level))
    db.commit()
    return cursor.lastrowid

def insert_table(seat1, seat2, seat3, seat4):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO tables (seat1, seat2, seat3, seat4) VALUES (?, ?, ?, ?)', 
                   (seat1, seat2, seat3, seat4))
    db.commit()
    return cursor.lastrowid

def mark_synced(table, id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'UPDATE {table} SET synced = 1 WHERE id = ?', (id,))
    db.commit()

def get_unsynced(table):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM {table} WHERE synced = 0')
    return cursor.fetchall()
