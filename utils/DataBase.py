import sqlite3


def create_database():
    db = sqlite3.connect("users_data.db")

    db.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        age INTEGER,
                        city_id INTEGER,
                        gender_id INTEGER,
                        status_id INTEGER);
                """)
    db.commit()

    db.execute("""CREATE TABLE IF NOT EXISTS users_match (
                        user_searching_id INTEGER,
                        user_id INTEGER, 
                        top_photos TEXT, 
                        is_seen BOOLEAN DEFAULT FALSE);
                """)
    db.commit()

    db.execute("""CREATE TABLE IF NOT EXISTS users_needs (
                            user_id INTEGER PRIMARY KEY,
                            age INTEGER,
                            city_id INTEGER,
                            gender_id INTEGER,
                            status_id INTEGER);
                    """)
    db.commit()

    db.close()


def user_exists(user_id):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id};")
    result = cursor.fetchall()
    print(result)
    db.close()
    return bool(result)


def add_user(user_id, age, city, gender, status):
    db = sqlite3.connect("users_data.db")
    db.execute(f"INSERT OR IGNORE INTO users VALUES ({user_id}, {age}, {city}, {gender}, {status});")
    db.commit()
    db.close()


def get_scope(user_id, scope):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT {scope} FROM users WHERE user_id = {user_id};")
    result = cursor.fetchall()
    print(result)
    db.close()
    return result[0][0]


def get_matches(user_id):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, top_photos FROM users_match WHERE user_searching_id = {user_id};")
    result = cursor.fetchall()
    db.close()
    return result


def get_seen_matches(user_id):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, top_photos FROM users_match WHERE user_searching_id = {user_id} and is_seen = TRUE;")
    result = cursor.fetchall()
    db.close()
    return result


def get_match(user_id):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, top_photos FROM users_match WHERE user_searching_id = {user_id} and is_seen = FALSE;")
    result = cursor.fetchone()
    cursor.execute(f"UPDATE users_match SET is_seen = TRUE WHERE user_searching_id = {user_id} and user_id = {result[0]};")
    db.commit()
    db.close()
    return result


def matches_exist(user_id):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users_match WHERE user_searching_id = {user_id} and is_seen = FALSE;")
    result = cursor.fetchall()
    db.close()
    return len(result) != 0


def update_user(user_id, scope, value):
    db = sqlite3.connect("users_data.db")
    db.execute(f"UPDATE users SET {scope} = {value} WHERE user_id = {user_id};")
    db.commit()
    db.close()


def add_match(user_searching_id, user_id, top_photos):
    db = sqlite3.connect("users_data.db")
    db.execute("INSERT OR IGNORE INTO users_match VALUES (?, ?, ?, FALSE);", (user_searching_id, user_id, f"{top_photos}"))
    db.commit()
    db.close()


def add_need(user_id):
    db = sqlite3.connect("users_data.db")
    db.execute(f"INSERT OR IGNORE INTO users_needs VALUES ({user_id}, 0, 0, 0, 0);")
    db.commit()
    db.close()


def update_need(user_id, scope, value):
    db = sqlite3.connect("users_data.db")
    db.execute(f"UPDATE users_needs SET {scope} = {value} WHERE user_id = {user_id};")
    db.commit()
    db.close()


def get_need(user_id, scope):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT {scope} FROM users_needs WHERE user_id = {user_id};")
    result = cursor.fetchall()
    db.close()
    return result[0][0]


def user_in_match(user_searching_id, user_id):
    db = sqlite3.connect("users_data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users_match WHERE user_searching_id = {user_searching_id} AND user_id = {user_id};")
    result = cursor.fetchall()
    db.close()
    return len(result) != 0


def clear_database():
    db = sqlite3.connect("users_data.db")
    db.execute("DROP TABLE IF EXISTS users;")
    db.execute("DROP TABLE IF EXISTS users_match;")
    db.commit()
    db.close()
