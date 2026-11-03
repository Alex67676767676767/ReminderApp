import sqlite3
import os
import sys

# Умный путь: если запущен как EXE, сохраняем базу рядом с ним. Если в PyCharm - в папке проекта.
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(application_path, "reminder.db")

# ... дальше идет твоя функция init_db() и остальной код без изменений ...


def init_db():
    """Создает таблицы, если их еще нет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Таблица напоминаний
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