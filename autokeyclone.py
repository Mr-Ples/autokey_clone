import keyboard

#
# def init_wlclip_clipboard():
#     DEFAULT_SELECTION = 'c'
#     PRIMARY_SELECTION = 'p'
#     ENCODING = 'utf-8'
#
#     def copy_wlclip(text, primary=False):
#         text = str(text)  # Converts non-str values to str.
#         selection = DEFAULT_SELECTION
#         if primary:
#             selection = PRIMARY_SELECTION
#         p = subprocess.Popen(
#             ['wlclip', '-selection', selection],
#             stdin=subprocess.PIPE, close_fds=True
#         )
#         p.communicate(input=text.encode('utf-8'))
#
#     def paste_wlclip(primary=False):
#         selection = DEFAULT_SELECTION
#         if primary:
#             selection = PRIMARY_SELECTION
#         p = subprocess.Popen(
#             ['wlclip', '-selection', selection, '-o'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             close_fds=True
#         )
#         stdout, stderr = p.communicate()
#         # Intentionally ignore extraneous output on stderr when clipboard is empty
#         return stdout.decode(ENCODING)
#
#     return copy_wlclip, paste_wlclip
#
#
# copy, paste = init_wlclip_clipboard()
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


def replace_stuff(event):
    if event.event_type == 'up':
        return

    try:
        print([elem.name for elem in     keyboard.stop_recording()])
    except:
        pass
    keyboard.press_and_release('backspace')
    for char in "We're glad your issue is resolved! If you are enjoying the game, please share your experience with a 5-Star review on the Store: https://l.linklyhq.com/l/1SFTp":
        if char.isupper():
            keyboard.press_and_release(f'shift+{char.lower()}')
        elif not char.isalpha():
            if SPECIAL_KEYS.get(char):
                keyboard.press_and_release(f'shift+{SPECIAL_KEYS[char]}')
            else:
                try:
                    keyboard.press(char)
                except Exception as err:
                    print(err)
                try:
                    keyboard.release(char)
                except Exception as err:
                    print(err)
        else:
            try:
                keyboard.press(char)
            except Exception as err:
                print(err)
            try:
                keyboard.release(char)
            except Exception as err:
                print(err)
    keyboard.start_recording()


recording = keyboard.start_recording()
keyboard.hook_key('1', replace_stuff)
keyboard.wait()
