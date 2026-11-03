import sqlite3
import os
import sys
import json

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(application_path, "reminder.db")




def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            datetime TEXT NOT NULL,
            sound TEXT DEFAULT 'default',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("База данных готова!")


def add_reminder(user_id, title, datetime_str, sound='default'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reminders (user_id, title, datetime, sound) VALUES (?, ?, ?, ?)",
        (user_id, title, datetime_str, sound)
    )
    conn.commit()
    conn.close()


def get_user_reminders(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, datetime FROM reminders WHERE user_id = ? ORDER BY datetime ASC", (user_id,))
    reminders = cursor.fetchall()
    conn.close()
    return reminders


def export_reminders_to_json(user_id):
    """Экспортирует напоминания пользователя в JSON файл"""
    reminders = get_user_reminders(user_id)

    data = []
    for r_id, title, dt in reminders:
        data.append({
            "id": r_id,
            "title": title,
            "datetime": dt
        })

    filename = f"reminders_export_user_{user_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        # ensure_ascii=False нужен, чтобы русские буквы сохранялись нормально, а не в виде \u0430\u0431...
        json.dump(data, f, ensure_ascii=False, indent=4)

    return filename