text = clipboard.get_clipboard()
response = "Greetings again %s, please confirm your issue has been resolved. Kind regards, MoMi Support. " % text
keyboard.send_keys("<ctrl>+v")
clipboard.fill_clipboard(response)
