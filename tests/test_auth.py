import pytest
import os
from auth import AuthManager
import sqlite3

# Для тестов используем отдельную базу, чтобы не ломать основную
TEST_DB = "test_reminder.db"


@pytest.fixture(autouse=True)
def setup_database():
    # Создаем временную базу перед тестом
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    auth = AuthManager(db_name=TEST_DB)

    yield auth  # Отдаем объект auth в тест

    # Удаляем временную базу после теста
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


# --- САМИ ТЕСТЫ ---

def test_valid_email(setup_database):
    """Тест проверки формата почты (Regex)"""
    auth = setup_database
    assert auth.is_valid_email("student@mail.ru") is True
    assert auth.is_valid_email("invalid-email.com") is False


def test_successful_registration(setup_database):
    """Тест успешной регистрации"""
    auth = setup_database
    success, message = auth.register_user("newuser@mail.ru", "securepassword")
    assert success is True
    assert message == "Успешная регистрация!"


def test_duplicate_email(setup_database):
    """Тест защиты от дубликатов почты"""
    auth = setup_database
    auth.register_user("duplicate@mail.ru", "pass123")
    success, message = auth.register_user("duplicate@mail.ru", "pass456")
    assert success is False
    assert message == "Пользователь с такой почтой уже существует"


def test_successful_login(setup_database):
    """Тест успешного входа с правильным паролем"""
    auth = setup_database
    auth.register_user("login@mail.ru", "mypassword")
    success, user_id = auth.login_user("login@mail.ru", "mypassword")
    assert success is True
    assert user_id is not None


def test_wrong_password_login(setup_database):
    """Тест неудачного входа с неправильным паролем"""
    auth = setup_database
    auth.register_user("wrong@mail.ru", "mypassword")
    success, user_id = auth.login_user("wrong@mail.ru", "wrongpassword")
    assert success is False
    assert user_id is None