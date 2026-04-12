from database.db import conn, cursor


# -----------------------------
# 💾 SAVE HISTORY
# -----------------------------
def save_history(username, score, feedback):

    try:
        cursor.execute(
            "INSERT INTO history (username, score, feedback) VALUES (?, ?, ?)",
            (username, score, feedback)
        )
        conn.commit()

    except Exception as e:
        print("Error saving history:", e)


# -----------------------------
# 📜 GET HISTORY
# -----------------------------
def get_history(username, limit=10):

    try:
        cursor.execute(
            """
            SELECT score, feedback, timestamp 
            FROM history 
            WHERE username=? 
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (username, limit)
        )

        results = cursor.fetchall()

        if not results:
            return []

        return results

    except Exception as e:
        print("Error fetching history:", e)
        return []