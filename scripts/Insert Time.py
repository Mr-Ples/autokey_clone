from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%H:%M")

keyboard.send_keys(dt_string)
