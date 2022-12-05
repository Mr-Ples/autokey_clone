import datetime
import os
import subprocess
import threading

import keyboard

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
            stderr=subprocess.PIPE
        )
        stdout, stderr = p.communicate()

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
            ['wl-paste']
        )
        p.communicate()

    return copy_wlclip, paste_wlclip


copy, paste = init_wlclip_clipboard() if os.getenv('XDG_SESSION_TYPE') == 'wayland' else init_xclip_clipboard()


def write(message: str):
    steps = []
    print('shift+1')
    print(keyboard.key_to_scan_codes('!'))

    for char in message:
        if char.isupper():
            steps.append(f'shift+{char.lower()}')
        elif not char.isalpha():
            if env.SPECIAL_KEYS.get(char):
                steps.append(f'shift+{env.SPECIAL_KEYS[char]}')
            else:
                steps.append(keyboard.key_to_scan_codes(char))
        else:
            steps.append(keyboard.key_to_scan_codes(char))

    for step in steps:
        try:
            keyboard.press(step)
        except Exception as err:
            print(err)

        try:
            keyboard.release(step)
        except Exception as err:
            print(err)


def send(message: str):
    log(message)
    copy(message)
    write(message)


def log(*args) -> None:
    with threading.Lock():
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0).time()} UTC] ', *args, flush=True)
        with open(f'{os.path.join(env.LOGS_PATH, str(env.LOGS_SESSION))}.txt', 'a+') as output:
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0).time()} UTC] ', *args, file=output)


def debug_log(*args) -> None:
    with open(f'{os.path.join(env.LOGS_PATH, str(env.LOGS_SESSION))}_DEBUG.txt', 'a+') as output:
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0).time()} UTC] ', *args, file=output)


def find_content(shortcut: str):
    """
    Gets the content form a shortcut if found in the key map file.
    """
    for data in env.KEY_MAP.values():
        for shortcuts in data.get("shortcut", []):
            if shortcut in shortcuts:
                return data['content']


def type_and_replace(shortcut: str):
    """
    Types the content corresponding to a given shortcut and removes the typed shortcut (also copies content to clipboard)
    """
    content = find_content(shortcut)
    if content:
        # for _ in range(len(shortcut)):
        #     keyboard.press_and_release('backspace')
        env.PRESSED_KEYS = []
        send(content)


def replace_stuff(event):
    global recording

    debug_log(event.__dict__)
    if event.event_type == 'up':
        return

    recorded_events_queue, hooked = recording
    keys = list(recorded_events_queue.queue)

    try:
        [env.PRESSED_KEYS.append(elem.name) for elem in keys if elem.event_type == 'down' and not elem.modifiers and elem.name != 'shift']
    except:
        pass
    log(env.PRESSED_KEYS)
    debug_log(keys)
    debug_log([key.modifiers for key in keys])
    if len(env.PRESSED_KEYS) > 1:
        for chunk_size in range(2, 5):
            debug_log(env.PRESSED_KEYS)
            if len(env.PRESSED_KEYS) < chunk_size:
                return
            chars = env.PRESSED_KEYS[-chunk_size:]
            combo = "".join(chars) + '!'
            log("combo:", combo)
            type_and_replace(combo)


recording = keyboard.start_recording()
keyboard.hook_key('1', replace_stuff)
keyboard.wait()
# W
