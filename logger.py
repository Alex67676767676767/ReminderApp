import logging
import os
import sys

# Умный путь для лог-файла (рядом с exe или в папке проекта)
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(application_path, "app.log")


def setup_logger():
    logger = logging.getLogger("ReminderApp")
    logger.setLevel(logging.INFO)

    # Чтобы обработчики не дублировались при перезапусках
    if not logger.handlers:
        # Запись в файл
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        # Вывод в консоль (чтобы мы видели логи в PyCharm)
        console_handler = logging.StreamHandler()

        # Формат: [Дата Время] - [Уровень] - Сообщение
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Создаем глобальный объект логгера, который будем импортировать в другие файлы
log = setup_logger()