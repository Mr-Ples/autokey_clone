from datetime import date

today = date.today()

d1 = today.strftime("%Y-%m-%d")

# output = system.exec_command("date")
keyboard.send_keys(d1)
