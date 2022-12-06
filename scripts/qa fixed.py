text = clipboard.get_clipboard()
response = "staging c582a01a ([see short video](%s))" % text
keyboard.send_keys("<ctrl>+v")
clipboard.fill_clipboard(response)
