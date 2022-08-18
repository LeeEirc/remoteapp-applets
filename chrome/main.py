import time
import sys
import os
import base64
import json

from selenium import webdriver

current_dir = os.path.dirname(__file__)
meta_file = os.path.join(current_dir, 'manifests.json')
meta_data = {
    'type': 'python',
    'protocols': ['web'],
}


class WebChrome(object):

    def __init__(self, username='', password='', url=''):
        self.driver = None
        self.username = username
        self.password = password
        self.url = url
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-dev-tools")

    def run(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get(self.url)
        self.driver.maximize_window()
        msg = "Unable to evaluate script: disconnected: not connected to DevTools\n"
        while True:
            time.sleep(5)
            logs = self.driver.get_log('driver')
            if len(logs) == 0:
                continue
            ret = logs[-1]
            if isinstance(ret, dict):
                if ret.get("message") == msg:
                    print(ret)
                    break
        self.driver.close()


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
    app = WebChrome(**data)
    app.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
