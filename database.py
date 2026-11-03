import sqlite3
import os

DB_NAME = "reminder.db"


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