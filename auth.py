import sqlite3
import bcrypt
import re


class AuthManager:
    def __init__(self, db_name="reminder.db"):
        self.db_name = db_name

    def is_valid_email(self, email):
        # Регулярное выражение для проверки почты
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def register_user(self, email, password):
        if not self.is_valid_email(email):
            return False, "Некорректный формат почты"

        # Хешируем пароль (превращаем в нечитаемый набор символов)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
            conn.close()
            return True, "Успешная регистрация!"
        except sqlite3.IntegrityError:
            return False, "Пользователь с такой почтой уже существует"
        except Exception as e:
            return False, f"Ошибка БД: {e}"

    def login_user(self, email, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_id, stored_hash = user
            # Проверяем, совпадает ли введенный пароль с хешем из базы
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                return True, user_id
        return False, None