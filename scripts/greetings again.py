text = clipboard.get_clipboard()
response = "Greetings again %s, " % text
#keyboard.send_keys(response)
keyboard.send_keys("<ctrl>+v")
clipboard.fill_clipboard(response)
