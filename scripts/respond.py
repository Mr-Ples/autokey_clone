text = clipboard.get_clipboard()
response = "Greetings again %s, please respond to the above questions so we can look into your issue. Kind regards, MoMi Support. " % text
keyboard.send_keys("<ctrl>+v")
clipboard.fill_clipboard(response)
