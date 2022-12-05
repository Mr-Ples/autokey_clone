import datetime
import os
import subprocess
import threading
import time

from pynput import keyboard

import env


def init_xclip_clipboard():
    DEFAULT_SELECTION = 'c'
    PRIMARY_SELECTION = 'p'
    ENCODING = 'utf-8'

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
        return stdout.decode(ENCODING)

    return copy_xclip, paste_xclip


copy, paste = init_xclip_clipboard()


def log(*args) -> None:
    with threading.Lock():
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0).time()} UTC] ', *args, flush=True)
        with open(f'{os.path.join(env.LOGS_PATH, str(env.LOGS_SESSION))}.txt', 'a+') as output:
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0).time()} UTC] ', *args, file=output)


def debug_log(*args) -> None:
    with open(f'{os.path.join(env.LOGS_PATH, str(env.LOGS_SESSION))}_DEBUG.txt', 'a+') as output:
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0).time()} UTC] ', *args, file=output)


def type_and_replace(shortcut: str):
    """
    Types the content corresponding to a given shortcut and removes the typed shortcut (also copies content to clipboard)
    """
    content = find_content(shortcut)
    if content:
        copy(content)
        for _ in range(len(shortcut) + 1):
            keyboard.Controller().tap(keyboard.Key.backspace)
        keyboard.Controller().type(content)


def find_content(shortcut: str):
    """
    Gets the content form a shortcut if found in the key map file.
    """
    for data in env.KEY_MAP.values():
        for shortcuts in data.get("shortcut", []):
            if shortcut in shortcuts:
                return data['content']


def on_press(key):
    try:
        env.KEY_PRESSED = key.char
        debug_log('Alphanumeric key pressed: {0} '.format(key.char))
    except AttributeError:
        env.KEY_PRESSED = key
        debug_log('special key pressed: {0}'.format(key))
    env.LATEST_KEY = env.KEY_PRESSED


def on_release(key):
    env.PRESSED_KEYS.append(key)
    if (len(env.PRESSED_KEYS) > 3
            and (keyboard.Key.shift in env.PRESSED_KEYS[-2:])
            and (keyboard.KeyCode.from_char('1') in env.PRESSED_KEYS[-2:])):
        for chunk_size in range(2, 5):
            debug_log(env.PRESSED_KEYS)
            if len(env.PRESSED_KEYS) < chunk_size:
                return
            combo = "".join([elem.char for elem in env.PRESSED_KEYS[-chunk_size - 2:-2]])
            log("combo:", combo)
            type_and_replace(combo)

    if key == keyboard.KeyCode.from_char('!'):
        for chunk_size in range(2, 5):
            debug_log(env.PRESSED_KEYS)
            if len(env.PRESSED_KEYS) < chunk_size:
                return
            combo = "".join([elem.char for elem in env.PRESSED_KEYS[-chunk_size - 1:]])
            log("combo:", combo)
            type_and_replace(combo)

    debug_log(f"released:{key}, !:{keyboard.KeyCode.from_char('!')}, {key == keyboard.KeyCode.from_char('!')}")


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    while True:
        time.sleep(0.44)
