import sys

from common import (block_input, unblock_input)
from common import (get_manifest_data, convert_base64_to_dict)

from app import AppletApplication

_default_path = r"C:\Program Files\PLSQL Developer 12\plsqldev.exe"

meta_data = {
    'path': _default_path,
    'connect_type': 'application',
    'exec_type': 'python',
    'protocols': ['oracle'],
}


def main():
    base64_str: str = sys.argv[1]
    meta_data.update(get_manifest_data())
    data = dict()
    data.update(convert_base64_to_dict(base64_str))
    data.update({"manifest": meta_data})
    app = AppletApplication(**data)
    block_input()
    app.run()
    unblock_input()
    app.wait()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
