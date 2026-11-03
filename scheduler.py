import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from PySide6.QtWidgets import QSystemTrayIcon


class NotificationManager:
    def __init__(self, tray_icon: QSystemTrayIcon):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.tray_icon = tray_icon

    def schedule_reminder(self, title, dt_str):
        try:
            # Превращаем строку "2026-03-12 22:47:28" в объект времени
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

            # Ставим задачу, если время еще не прошло
            if dt > datetime.datetime.now():
                self.scheduler.add_job(
                    self.show_notification,
                    'date',
                    run_date=dt,
                    args=[title]
                )
                print(f"Задача на {dt_str} ('{title}') успешно запланирована!")
            else:
                print(f"Время для '{title}' уже прошло, уведомление не поставлено.")
        except Exception as e:
            print(f"Ошибка планировщика: {e}")

    def show_notification(self, title):
        # Показываем системное уведомление Windows
        self.tray_icon.showMessage(
            "Напоминание!",
            title,
            QSystemTrayIcon.MessageIcon.Information,
            10000  # Показывать 10 секунд
        )
        # Включаем системный звук (пока просто пик, потом добавим красивые mp3)
        import winsound
        winsound.MessageBeep(winsound.MB_ICONASTERISK)