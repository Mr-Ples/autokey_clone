import keyboard

import env

for data in env.KEY_MAP.values():
    for shortcuts in data.get("shortcut", []):
        if data.get('content'):
            keyboard.add_abbreviation(shortcuts, data['content'], match_suffix=True)
keyboard.wait()
