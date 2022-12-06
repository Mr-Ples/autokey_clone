import os
from typing import List
import os
import json
import traceback
import re

DATA_DICT = {}
query = 'pending'

# Location to Autokey data dir - You can set it manually
USER = os.getenv('USER')
AUTOKEY_DATA_DIR = os.path.join('.config', 'autokey', 'data')

class AutokeyEntry:
    """
    Object representing Autokey entries
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.content = ""
        self.shortcut = ["None"]

    def __str__(self) -> str:
        return "\n=============================================================\n" + str([sc for sc in self.shortcut]) + "\t" + self.name + "\n\n" + self.content


def populate_data_file():
    """
    List all phrases and scripts located in the data dir
    """
    # List all phrases and scripts located in the data dir
    for subdir, dirs, files in os.walk(AUTOKEY_DATA_DIR):
        for file in files:
            try:
                file_path = os.path.join(subdir, file)
                if file.startswith('.'):
                    file = file[1:]
                file_name, ext = file.split('.')
                print()
                print(file_name)
                print(file_path)

                if not DATA_DICT.get(file_name):
                    print("new file name:", DATA_DICT.keys())
                    DATA_DICT.update({file_name: AutokeyEntry(file_name)})
                if ext == 'json':
                    print('json')
                    with open(file_path) as file_reader:
                        json_data = json.load(file_reader)
                        active = json_data['modes']
                        if active:
                            shortcut = json_data['abbreviation']['abbreviations']
                            print("shortcut:", shortcut)
                            DATA_DICT[file_name].shortcut = shortcut
                if ext == 'txt':
                    with open(file_path) as file_reader:
                        content = file_reader.read()
                        print('content: ', content)
                        DATA_DICT[file_name].content = content
            except:
                print('==========================================')
                traceback.print_exc()
                print(subdir, dirs, files)
                print('==========================================')

    print(str(DATA_DICT))

def find_entry(find: str) -> List[str]:
    """
    Finds the given substring in the name or content or shortcut of all entries
    """
    found_entries = []
    # Currently check find against file path and name only
    for entry_name, entry in DATA_DICT.items():
        if not entry.content:
            continue
        if (re.search(find, entry_name, flags=re.IGNORECASE)
                or re.search(find, entry.content, flags=re.IGNORECASE)
                or re.search(find, str(entry.shortcut), flags=re.IGNORECASE)):
            found_entries.append(entry)
    return found_entries

# Autokey scripting API: https://autokey.github.io/lib.scripting-module.html
# Zenity: https://linux.die.net/man/1/zenity
populate_data_file()
while True:
    ret_code, query = dialog.input_dialog(title="Search",
                                          message='Enter a query')
    if ret_code != 0:
        exit(1)

    found = find_entry(query)
    dialog.info_dialog("Window information", "".join([str(found_entry) for found_entry in found]))
