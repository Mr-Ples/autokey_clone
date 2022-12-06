import datetime
import json
import os
import subprocess

import keyboard

HOME = os.path.abspath(".")
print(HOME)
if not os.path.isdir(HOME):
    os.mkdir(HOME)

LOGS_SESSION = datetime.datetime.now().date()
LOGS_PATH = os.path.join(HOME, 'logs')
if not os.path.isdir(LOGS_PATH):
    os.mkdir(LOGS_PATH)

KEY_MAP_PATH = os.path.join(HOME, 'key_map.json')
if not os.path.isfile(KEY_MAP_PATH):
    with open(KEY_MAP_PATH, 'w+') as file:
        file.write('{}')

with open(KEY_MAP_PATH, 'r') as file:
    KEY_MAP = json.load(file)

SPECIAL_KEYS = {
    '`': '`',
    '!': '1',
    '@': '2',
    '#': '3',
    '$': '4',
    '%': '5',
    '^': '6',
    '&': '7',
    '*': '8',
    '(': '9',
    ')': '0',
    '_': '-',
    '+': '=',
    '{': '[',
    '}': ']',
    '|': '\\',
    ':': ';',
    '"': '\'',
    '<': ',',
    '>': '.',
    '?': '/',
}

PRESSED_KEYS = []


def init_xclip_clipboard():
    DEFAULT_SELECTION = 'c'
    PRIMARY_SELECTION = 'p'

    def copy_xclip(text, primary=False):
        text = str(text)  # Converts non-str values to str.
        selection = DEFAULT_SELECTION
        if primary:
            selection = PRIMARY_SELECTION
        p = subprocess.Popen(
            ['xclip', '-selection', selection],
            stdin=subprocess.PIPE, close_fds=True
        )
        p.communicate(input=text.encode('utf-8'))

    def paste_xclip(primary=False):
        selection = DEFAULT_SELECTION
        if primary:
            selection = PRIMARY_SELECTION
        p = subprocess.Popen(
            ['xclip', '-selection', selection, '-o'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True
        )
        stdout, stderr = p.communicate()
        # Intentionally ignore extraneous output on stderr when clipboard is empty
        return stdout.decode('utf-8')

    return copy_xclip, paste_xclip


def init_wlclip_clipboard():
    def copy_wlclip(text):
        text = str(text)  # Converts non-str values to str.
        p = subprocess.Popen(
            ['wl-copy'],
            stdin=subprocess.PIPE, close_fds=True
        )
        p.communicate(input=text.encode('utf-8'))

    def paste_wlclip():
        p = subprocess.Popen(
            ['wl-paste'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True
        )
        stdout, stderr = p.communicate()
        # Intentionally ignore extraneous output on stderr when clipboard is empty
        return stdout.decode('utf-8')

    return copy_wlclip, paste_wlclip


copy, paste = init_wlclip_clipboard() if not os.getenv('XDG_CURRENT_DESKTOP') else init_xclip_clipboard()


def control_v():
    keyboard.press('ctrl')
    keyboard.press_and_release('v')
    keyboard.release('ctrl')
