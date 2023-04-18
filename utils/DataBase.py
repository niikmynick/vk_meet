import sqlite3


def create_database():
    db = sqlite3.connect("users_data.db")

    db.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        age INTEGER,
                        city TEXT,
                        gender INTEGER,
                        status INTEGER);
                """)
    db.commit()

    db.execute("""CREATE TABLE IF NOT EXISTS users_match (
                        user_searching_id INTEGER PRIMARY KEY,
                        user_id INTEGER);
                """)
    db.commit()

    db.execute("""CREATE TABLE IF NOT EXISTS users_needs (
                            user_id INTEGER PRIMARY KEY,
                            age INTEGER,
                            city TEXT,
                            gender INTEGER,
                            status INTEGER);
                    """)
    db.commit()

    db.close()


def add_user(user_id, age, city, gender, status):
    db = sqlite3.connect("users_data.db")
    db.execute(f"INSERT OR IGNORE INTO users VALUES ({user_id}, {age}, {city}, {gender}, {status})")
    db.commit()
    db.close()


def get_scope(user_id, scope):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT {scope} FROM users WHERE user_id = {user_id}")
    result = cursor.fetchall()
    db.close()
    return result[0][0]


def get_matches(user_id):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM users_match WHERE user_searching_id = {user_id}")
    result = cursor.fetchall()
    db.close()
    return result


def update_user(user_id, scope, value):
    db = sqlite3.connect("users_data.db")
    db.execute(f"UPDATE users SET {scope} = {value} WHERE user_id = {user_id}")
    db.commit()
    db.close()


def add_match(user_searching_id, user_id):
    db = sqlite3.connect("users_data.db")
    db.execute(f"INSERT OR IGNORE INTO users_match VALUES ({user_searching_id}, {user_id})")
    db.commit()
    db.close()


def user_in_match(user_searching_id, user_id):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users_match WHERE user_searching_id = {user_searching_id} AND user_id = {user_id}")
    result = cursor.fetchall()
    db.close()
    return len(result) != 0


def clear_database():
    db = sqlite3.connect("users_data.db")
    db.execute("DROP TABLE IF EXISTS users")
    db.execute("DROP TABLE IF EXISTS users_match")
    db.commit()
    db.close()
