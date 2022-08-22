import time
import sys
import os
import base64
import json
from subprocess import CREATE_NO_WINDOW

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from common import notify_err_message

current_dir = os.path.dirname(__file__)
meta_file = os.path.join(current_dir, 'manifests.json')
meta_data = {
    'type': 'python',
    'protocols': ['web'],
}


class StepAction:
    find_methods = {
        "NAME": By.NAME,
        "ID": By.ID,
        "CLASS_NAME": By.CLASS_NAME,
        "CSS_SELECTOR": By.CSS_SELECTOR,
        "XPATH": By.XPATH
    }

    def __init__(self, identifier='', by='ID', value='', action='input', **kwargs):
        self.identifier = identifier
        self.by = by
        self.value = value
        self.action = action

    def execute(self, driver: webdriver.Chrome):

        ele = driver.find_element(by=self.find_methods[self.by], value=self.identifier)
        if not ele:
            return False
        if self.action == 'input':
            ele.send_keys(self.value)
        elif self.action in ['click', 'button']:
            ele.click()
        return True


def execute_action(driver: webdriver.Chrome, step: StepAction):
    try:
        step.execute(driver)
    except Exception as e:
        print(e)
        notify_err_message(str(e))


def read_app_jsons(app_dir):
    ret = dict()
    for file in os.listdir(app_dir):
        if not file.endswith('.json'):
            continue
        with open(os.path.join(app_dir, file), 'r', encoding='utf8') as f:
            data = json.load(f)
            ret.update(data)
    return ret


class WebChrome(object):

    def __init__(self, name='', username='', password='', url='', **kwargs):
        self.driver = None
        self.username = username
        self.password = password
        self.url = url
        self.name = name
        web_app_dir = os.path.join(current_dir, name)

        self._app_datas = read_app_jsons(web_app_dir)

        self._steps = sorted(self._app_datas['steps'], key=lambda item: item['step'])

        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self._chrome_options.add_argument("start-maximized")
        self._chrome_options.add_argument("--disable-extensions")
        self._chrome_options.add_argument("--disable-dev-tools")
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        self._chrome_options.add_experimental_option("prefs", prefs)

    def run(self):
        service = Service()
        service.creationflags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(options=self._chrome_options, service=service)
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        for step in self._steps:
            val = step['value']
            if val:
                step['value'] = val.replace("{password}", self.password)
            action = StepAction(**step)
            execute_action(self.driver, action)

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
