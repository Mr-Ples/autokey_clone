import subprocess
import env
import keyboard


def init_wlclip_clipboard():
    ENCODING = 'utf-8'

    def copy_wlclip(text):
        text = str(text)  # Converts non-str values to str.
        p = subprocess.Popen(
            ['wl-copy'],
            stdin=subprocess.PIPE, close_fds=True
        )
        p.communicate(input=text.encode('utf-8'))

    def paste_wlclip():
        keyboard.press('control')
        keyboard.press_and_release('v')
        keyboard.release('control')

    return copy_wlclip, paste_wlclip


copy, paste = init_wlclip_clipboard()


def replace_stuff(event):
    if event.event_type == 'up':
        return

    try:
        print([elem.name for elem in keyboard.stop_recording()])
    except:
        pass
    copy("We're glad your issue is resolved! If you are enjoying the game, please share your experience with a 5-Star review on the Store: https://l.linklyhq.com/l/1SFTp")
    paste()
    # for char in "We're glad your issue is resolved! If you are enjoying the game, please share your experience with a 5-Star review on the Store: https://l.linklyhq.com/l/1SFTp":
    #     if char.isupper():
    #         keyboard.press_and_release(f'shift+{char.lower()}')
    #     elif not char.isalpha():
    #         if env.SPECIAL_KEYS.get(char):
    #             keyboard.press_and_release(f'shift+{env.SPECIAL_KEYS[char]}')
    #         else:
    #             try:
    #                 keyboard.press(char)
    #             except Exception as err:
    #                 print(err)
    #             try:
    #                 keyboard.release(char)
    #             except Exception as err:
    #                 print(err)
    #     else:
    #         try:
    #             keyboard.press(char)
    #         except Exception as err:
    #             print(err)
    #         try:
    #             keyboard.release(char)
    #         except Exception as err:
    #             print(err)
    keyboard.start_recording()


recording = keyboard.start_recording()
keyboard.hook_key('1', replace_stuff)
keyboard.wait()
