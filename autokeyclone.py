import datetime
import os
import threading

import keyboard

import env


def write(message: str):
    keyboard.write(message)
    steps = []

    for char in message:
        if char.isupper():
            steps.append(f'shift+{char.lower()}')
        elif not char.isalpha():
            if env.SPECIAL_KEYS.get(char):
                steps.append(f'shift+{env.SPECIAL_KEYS[char]}')
            else:
                steps.append(char)
        else:
            steps.append(char)

    for step in steps:
        try:
            keyboard.press(step)
            keyboard.release(step)
        except Exception as err:
            print(err)

    for char in message:
        try:
            keyboard._os_keyboard.type_unicode(char)
        except:
            pass


def send(message: str):
    log(message)
    env.copy(message)
    env.control_v()


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
                if data.get('content'):
                    return data['content']
                elif data.get('script'):
                    remove_abbr(shortcut)
                    exec(open(os.path.join('scripts', data.get('script'))).read())


def remove_abbr(abbr: str):
    for _ in range(len(abbr)):
        keyboard.press_and_release('backspace')


def type_and_replace(shortcut: str):
    """
    Types the content corresponding to a given shortcut and removes the typed shortcut (also copies content to clipboard)
    """
    content = find_content(shortcut)
    if content:
        remove_abbr(shortcut)
        env.PRESSED_KEYS = []
        send(content)
        return True


def replace_stuff(event):
    global recording

    if os.getenv('XDG_CURRENT_DESKTOP'):
        env.control_v()

    debug_log(event.__dict__)
    if event.event_type == 'up':
        return

    recorded_events_queue, hooked = recording
    keys = list(recorded_events_queue.queue)

    try:
        [env.PRESSED_KEYS.append((elem.name, elem.modifiers)) for elem in keys if elem.event_type == 'down' and elem.name != 'shift']
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
            print()
            chars = []
            for char, modif in env.PRESSED_KEYS[-chunk_size:]:
                print(char, modif, char.isalpha(), 'shift' in modif)
                if char.isalpha() and 'shift' in modif:
                    chars.append(char.upper())
                else:
                    chars.append(char)
            combo = "".join(chars) + '!'
            log("combo:", combo)
            if type_and_replace(combo):
                break


recording = keyboard.start_recording()
keyboard.hook_key('1', replace_stuff)

keyboard.wait()

"""
We are looking into your issue and will get back to you as soon as we can. It might take a while to get to your issue. 
"""
