import sys
import json
import base64
import os

if sys.platform == 'win32':
    from pywinauto import Application

#   process = subprocess.Popen([prog_path, ],
#                                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
#   process.wait()


_default_path = r"C:\Program Files\PLSQL Developer 12\plsqldev.exe"

current_dir = os.path.dirname(__file__)
meta_file = os.path.join(current_dir, 'manifests.json')
meta_data = {
    'path': _default_path,
    'type': 'python',
    'protocols': ['oracle'],
}


class OraclePLSQL(object):

    def __init__(self, path=_default_path, username="", password='',
                 host='', port='', db='', **kwargs):
        self.path = path
        if not self.path:
            self.path = _default_path
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db = db

    def run(self):
        app = Application(backend='uia')
        app.start(self.path)
        app.Dialog.wait('ready', )
        url = "{}:{}/{}".format(self.host, self.port, self.db)
        app.Dialog.Edit1.set_text(self.password)
        app.Dialog.Edit2.set_text(self.username)
        app.Dialog.Edit3.set_text(url)
        app.Dialog.Button4.click()


def get_default_meta():
    ret = {}
    ret.update(meta_data)
    try:
        with open(meta_file, "r", encoding='utf8') as f:
            file_data = json.load(f)
            ret.update(file_data)
    except Exception as e:
        print(e)
    return ret


def parse_base64_str(base64_str: str) -> dict:
    try:
        data_json = base64.decodebytes(base64_str.encode('utf-8')).decode('utf-8')
        return json.loads(data_json)
    except Exception as e:
        print(e)
    return {}


def main():
    data = get_default_meta()
    if len(sys.argv) >= 2:
        base64_str = sys.argv[1]
        data.update(parse_base64_str(base64_str))
    app = OraclePLSQL(**data)
    app.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
