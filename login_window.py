import random
from PySide6.QtWidgets import QWidget, QVBoxLayout, QInputDialog
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (LineEdit, PasswordLineEdit, PrimaryPushButton,
                            PushButton, SubtitleLabel, setTheme, Theme, InfoBar)
from auth import AuthManager
from mailer import send_verification_email
from logger import log


class LoginWindow(QWidget):
    login_successful = Signal(int)

    def __init__(self):
        super().__init__()
        self.auth = AuthManager()
        self.setWindowTitle("Вход в Ежедневник")
        self.resize(400, 500)
        setTheme(Theme.LIGHT)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        self.title = SubtitleLabel("Ежедневник")
        self.email_input = LineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = PasswordLineEdit()
        self.password_input.setPlaceholderText("Пароль")

        self.btn_login = PrimaryPushButton("Войти")
        self.btn_register = PushButton("Зарегистрироваться")

        layout.addWidget(self.title, alignment=Qt.AlignCenter)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_register)

        self.btn_login.clicked.connect(self.handle_login)
        self.btn_register.clicked.connect(self.handle_register)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        success, user_id = self.auth.login_user(email, password)

        if success:
            self.login_successful.emit(user_id)
            self.close()
        else:
            InfoBar.error(title="Ошибка", content="Неверная почта или пароль", parent=self)

    def handle_register(self):
        email = self.email_input.text()
        password = self.password_input.text()

        # 1. Сначала проверяем, корректна ли почта (чтобы не отправлять письмо в пустоту)
        if not self.auth.is_valid_email(email):
            InfoBar.error(title="Ошибка", content="Некорректный формат почты", parent=self)
            return

        # 2. Генерируем 4-значный код
        verification_code = str(random.randint(1000, 9999))
        log.info(f"Сгенерирован код для {email}")

        # 3. Отправляем письмо
        InfoBar.info(title="Отправка...", content="Отправляем код на вашу почту...", parent=self)

        if send_verification_email(email, verification_code):
            # 4. Если письмо ушло, просим ввести код
            user_code, ok = QInputDialog.getText(self, "Подтверждение", "Введите 4-значный код из письма:")

            if ok and user_code == verification_code:
                # Код верный! Регистрируем
                success, message = self.auth.register_user(email, password)
                if success:
                    InfoBar.success(title="Успех", content=message, parent=self)
                else:
                    InfoBar.error(title="Ошибка БД", content=message, parent=self)
            else:
                InfoBar.error(title="Ошибка", content="Неверный код подтверждения", parent=self)
        else:
            InfoBar.error(title="Ошибка сети", content="Не удалось отправить письмо. Проверьте интернет.", parent=self)