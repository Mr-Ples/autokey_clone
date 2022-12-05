import json
import os
import datetime

HOME = os.path.abspath(".")
print(HOME)
if not os.path.isdir(HOME):
    os.mkdir(HOME)

LOGS_SESSION = datetime.datetime.now().replace(microsecond=0)
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
