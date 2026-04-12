from database.db import conn, cursor
import hashlib


# -----------------------------
# 🔐 HASH PASSWORD
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -----------------------------
# 📝 REGISTER
# -----------------------------
def register(username, password):

    try:
        hashed = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()

        return True

    except Exception as e:
        print("Register error:", e)
        return False


# -----------------------------
# 🔑 LOGIN
# -----------------------------
def login(username, password):

    try:
        hashed = hash_password(password)

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hashed)
        )

        return cursor.fetchone()

    except Exception as e:
        print("Login error:", e)
        return None