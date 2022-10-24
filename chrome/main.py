import sys

from common import (block_input, unblock_input)
from common import (get_manifest_data, convert_base64_to_dict)
from app import AppletApplication

meta_data = {
    'protocols': ['web'],
    'exec_type': 'python',
    'connect_type': 'web'
}


def main():
    base64_str = sys.argv[1]
    meta_data.update(get_manifest_data())
    data = dict()
    data.update(convert_base64_to_dict(base64_str))
    data.update({"manifest": meta_data})
    chrome_app = AppletApplication(**data)
    block_input()
    chrome_app.run()
    unblock_input()
    chrome_app.wait()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
