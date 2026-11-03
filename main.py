import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidgetItem, QSystemTrayIcon
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor  # Для создания иконки
from PySide6.QtCore import Qt
from qfluentwidgets import (FluentWindow, PrimaryPushButton, setTheme, Theme,
                            FluentIcon, SubtitleLabel, ListWidget)
from database import init_db, get_user_reminders
from login_window import LoginWindow
from reminder_dialog import ReminderDialog
from scheduler import NotificationManager


class MainWindow(FluentWindow):
    def __init__(self, user_id, notifier):
        super().__init__()
        self.user_id = user_id
        self.notifier = notifier
        self.setWindowTitle("Ежедневник")
        self.resize(900, 600)
        setTheme(Theme.LIGHT)

        self.homeWidget = QWidget()
        self.homeWidget.setObjectName("homeWidget")

        self.vBoxLayout = QVBoxLayout(self.homeWidget)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)

        self.titleLabel = SubtitleLabel("Мои напоминания")
        self.btn = PrimaryPushButton(FluentIcon.ADD, "Добавить напоминание")
        self.listWidget = ListWidget()

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.btn)
        self.vBoxLayout.addWidget(self.listWidget)

        self.addSubInterface(self.homeWidget, FluentIcon.HOME, "Главная")
        self.btn.clicked.connect(self.open_add_dialog)

        self.load_reminders()

    def open_add_dialog(self):
        self.dialog = ReminderDialog(self.user_id, self.on_reminder_added)
        self.dialog.show()

    def on_reminder_added(self):
        self.load_reminders()

    def load_reminders(self):
        self.listWidget.clear()
        reminders = get_user_reminders(self.user_id)
        for r_id, title, dt in reminders:
            item = QListWidgetItem(f"{dt} — {title}")
            self.listWidget.addItem(item)
            self.notifier.schedule_reminder(title, dt)


# Функция для создания простой иконки
def create_app_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setBrush(QColor(0, 120, 212))  # Синий цвет Windows
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, 64, 64)
    painter.end()
    return QIcon(pixmap)


if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)

    # Устанавливаем иконку для всего приложения
    app_icon = create_app_icon()
    app.setWindowIcon(app_icon)

    # Создаем иконку в трее с нашей картинкой
    tray_icon = QSystemTrayIcon(app_icon, app)
    tray_icon.setToolTip("Ежедневник запущен")
    tray_icon.show()

    notifier = NotificationManager(tray_icon)

    login_win = LoginWindow()
    main_win = None


    def open_main(user_id):
        global main_win
        main_win = MainWindow(user_id, notifier)
        main_win.show()


    login_win.login_successful.connect(open_main)
    login_win.show()
    sys.exit(app.exec())