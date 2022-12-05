import json
import os

HOME = os.path.abspath(".")
print(HOME)
if not os.path.isdir(HOME):
    os.mkdir(HOME)

KEY_MAP_PATH = os.path.join(HOME, 'key_map.json')
if not os.path.isfile(KEY_MAP_PATH):
    with open(KEY_MAP_PATH, 'w+') as file:
        file.write('{}')

with open(KEY_MAP_PATH, 'r') as file:
    KEY_MAP = json.load(file)
