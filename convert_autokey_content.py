import json
import os
import traceback

DATA_DICT = {}
query = 'pending'

# Location to Autokey data dir - You can set it manually
AUTOKEY_DATA_DIR = os.path.join('/home', 'simonl', '.config', 'autokey', 'data')
print(AUTOKEY_DATA_DIR)


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
                # print()
                # print(file_name)
                # print(file_path)

                if not DATA_DICT.get(file_name):
                    # print("new file name:", DATA_DICT.keys())
                    DATA_DICT.update({file_name: {}})
                if ext == 'json':
                    # print('json')
                    with open(file_path) as file_reader:
                        json_data = json.load(file_reader)
                        active = json_data['modes']
                        if active:
                            shortcut = json_data['abbreviation']['abbreviations']
                            # print("shortcut:", shortcut)
                            DATA_DICT[file_name]['shortcut'] = shortcut
                if ext == 'txt':
                    with open(file_path) as file_reader:
                        content = file_reader.read()
                        # print('content: ', content)
                        DATA_DICT[file_name]['content'] = content
            except:
                print('==========================================')
                traceback.print_exc()
                print(subdir, dirs, files)
                print('==========================================')

    open('key_map_converted.json', 'w+').write(json.dumps(DATA_DICT, indent=4))


populate_data_file()
