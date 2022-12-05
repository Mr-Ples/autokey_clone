import os
import datetime

PRESSED_KEYS = []
KEY_PRESSED = None
HOME = os.path.abspath(".")
print(HOME)
if not os.path.isdir(HOME):
    os.mkdir(HOME)

LOGS_SESSION = datetime.datetime.now().replace(microsecond=0)
LOGS_PATH = os.path.join(HOME, 'logs')
if not os.path.isdir(LOGS_PATH):
    os.mkdir(LOGS_PATH)

KEY_MAP = {
    "test": "this should be here"
}
