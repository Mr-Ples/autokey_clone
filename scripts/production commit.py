import os

user_home = os.path.expanduser('~/')
momi_version_path = os.path.join(user_home, 'bin', 'projects', 'python_scripts', 'data', 'MomiVersion.txt')
version = open(momi_version_path, 'r').read()
clipboard.fill_clipboard(version)
keyboard.send_keys(version)
