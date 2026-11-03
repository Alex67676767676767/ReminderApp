import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from PySide6.QtWidgets import QSystemTrayIcon
from logger import log  # <-- Добавили импорт

class NotificationManager:
    def __init__(self, tray_icon: QSystemTrayIcon):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.tray_icon = tray_icon
        log.info("Планировщик запущен.") # <-- Лог

    def schedule_reminder(self, title, dt_str):
        try:
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            if dt > datetime.datetime.now():
                self.scheduler.add_job(self.show_notification, 'date', run_date=dt, args=[title])
                log.info(f"Запланировано напоминание: '{title}' на {dt_str}") # <-- Лог
            else:
                log.warning(f"Время для '{title}' уже прошло, не запланировано.")
        except Exception as e:
            log.error(f"Ошибка планировщика: {e}")

    def show_notification(self, title):
        log.info(f"СРАБОТАЛО УВЕДОМЛЕНИЕ: '{title}'") # <-- Лог
        self.tray_icon.showMessage("Напоминание!", title, QSystemTrayIcon.MessageIcon.Information, 10000)
        import winsound
        winsound.MessageBeep(winsound.MB_ICONASTERISK)