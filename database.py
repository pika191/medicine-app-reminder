import sqlite3

def create_db():
    conn = sqlite3.connect('medication_history.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history
                      (date TEXT, medicine TEXT, dose TEXT)''')
    conn.commit()
    conn.close()

def save_history(medicine, dose):
    conn = sqlite3.connect('medication_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO history (date, medicine, dose) VALUES (datetime("now"), ?, ?)', (medicine, dose))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('medication_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM history')
    records = cursor.fetchall()
    conn.close()
    return records
