from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (LineEdit, PasswordLineEdit, PrimaryPushButton,
                            PushButton, SubtitleLabel, setTheme, Theme, InfoBar, InfoBarPosition)
from auth import AuthManager


class LoginWindow(QWidget):
    # Сигнал, который сообщит главному окну, что мы вошли
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

        # Привязываем кнопки к функциям
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_register.clicked.connect(self.handle_register)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        success, user_id = self.auth.login_user(email, password)

        if success:
            self.login_successful.emit(user_id)  # Отправляем сигнал главному окну
            self.close()
        else:
            InfoBar.error(title="Ошибка", content="Неверная почта или пароль", parent=self)

    def handle_register(self):
        email = self.email_input.text()
        password = self.password_input.text()
        success, message = self.auth.register_user(email, password)

        if success:
            InfoBar.success(title="Успех", content=message, parent=self)
        else:
            InfoBar.error(title="Ошибка", content=message, parent=self)