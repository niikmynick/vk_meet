import sqlite3


def create_database():
    conn = sqlite3.connect("users_data.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        age INTEGER,
                        city TEXT,
                        gender INTEGER,
                        status INTEGER);
                """)
    conn.commit()
    conn.close()

def insert_user(user_id, age, city, gender, status):
    conn = sqlite3.connect("users_data.db")
    conn.execute(f"INSERT INTO users VALUES ({user_id}, {age}, '{city}', {gender}, {status})")
    conn.commit()
    conn.close()

def user_exists(user_id):
    conn = sqlite3.connect("users_data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    data = cursor.fetchone()
    conn.close()
    return data