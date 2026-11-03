from PySide6.QtWidgets import QWidget, QVBoxLayout, QDateTimeEdit
from PySide6.QtCore import Qt, QDateTime, QTime  # Добавили QTime
from qfluentwidgets import LineEdit, PrimaryPushButton, SubtitleLabel, setTheme, Theme


class ReminderDialog(QWidget):
    def __init__(self, user_id, on_success_callback):
        super().__init__()
        self.user_id = user_id
        self.on_success = on_success_callback

        self.setWindowTitle("Новое напоминание")
        self.resize(400, 250)
        setTheme(Theme.LIGHT)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.title_label = SubtitleLabel("Добавить напоминание")
        self.input_title = LineEdit()
        self.input_title.setPlaceholderText("Название (например: Встреча)")

        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        self.date_edit.setCalendarPopup(True)

        self.btn_save = PrimaryPushButton("Сохранить")

        layout.addWidget(self.title_label)
        layout.addWidget(self.input_title)
        layout.addWidget(self.date_edit)
        layout.addWidget(self.btn_save)

        self.btn_save.clicked.connect(self.save_reminder)

    def save_reminder(self):
        from database import add_reminder

        title = self.input_title.text()
        if not title:
            return

            # Берем выбранную дату
        qdt = self.date_edit.dateTime()
        # Принудительно ставим ровно 00 секунд!
        qdt.setTime(QTime(qdt.time().hour(), qdt.time().minute(), 0))

        # Сохраняем в базу
        dt = qdt.toString("yyyy-MM-dd HH:mm:ss")
        add_reminder(self.user_id, title, dt)
        self.on_success()
        self.close()