import sqlite3
import bcrypt
import re
from logger import log  # <-- Добавили импорт


class AuthManager:
    def __init__(self, db_name="reminder.db"):
        self.db_name = db_name

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def register_user(self, email, password):
        log.info(f"Попытка регистрации: {email}")
        if not self.is_valid_email(email):
            log.warning(f"Ошибка регистрации: некорректный email {email}")
            return False, "Некорректный формат почты"

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        conn = None  # Объявляем заранее
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
            log.info(f"Успешная регистрация: {email}")
            return True, "Успешная регистрация!"
        except sqlite3.IntegrityError:
            log.warning(f"Ошибка регистрации: {email} уже существует")
            return False, "Пользователь с такой почтой уже существует"
        except Exception as e:
            log.error(f"Ошибка БД при регистрации: {e}")
            return False, f"Ошибка БД: {e}"
        finally:
            # ЭТОТ БЛОК ВЫПОЛНИТСЯ ВСЕГДА, ЗАКРЫВАЯ БАЗУ
            if conn:
                conn.close()

    def login_user(self, email, password):
        log.info(f"Попытка входа: {email}")  # <-- Лог
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_id, stored_hash = user
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                log.info(f"Успешный вход: {email}")  # <-- Лог
                return True, user_id

        log.warning(f"Неудачный вход: {email}")  # <-- Лог
        return False, None