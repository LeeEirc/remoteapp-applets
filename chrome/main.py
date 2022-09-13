import time
import sys
import os
import base64
import json
from enum import Enum
from subprocess import CREATE_NO_WINDOW

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import argparse

from common import (notify_err_message, block_input, unblock_input,
                    terminate_rdp_session)

current_dir = os.path.dirname(__file__)
meta_file = os.path.join(current_dir, 'manifests.json')
meta_data = {
    'type': 'python',
    'protocols': ['web'],
}


class Command(Enum):
    TYPE = 'type'
    CLICK = 'click'


def _execute_type(ele: WebElement, value: str):
    ele.send_keys(value)


def _execute_click(ele: WebElement, value: str):
    ele.click()


commands_func_maps = {
    Command.CLICK: _execute_click,
    Command.TYPE: _execute_type,
}


class StepAction:
    methods_map = {
        "NAME": By.NAME,
        "ID": By.ID,
        "CLASS_NAME": By.CLASS_NAME,
        "CSS_SELECTOR": By.CSS_SELECTOR,
        "XPATH": By.XPATH
    }

    def __init__(self, target='', value='', command=Command.TYPE, **kwargs):
        self.target = target
        self.value = value
        self.command = command

    def execute(self, driver: webdriver.Chrome) -> bool:
        if self.target == '' or (not self.target):
            return True
        target_name, target_value = self.target.split("=", 1)
        ele = driver.find_element(by=self.methods_map[target_name.upper()], value=target_value)
        if not ele:
            return False
        if self.command == 'type':
            ele.send_keys(self.value)
        elif self.command in ['click', 'button']:
            ele.click()
        return True

    def _execute_command_type(self, ele, value):
        ele.send_keys(value)


def execute_action(driver: webdriver.Chrome, step: StepAction) -> bool:
    try:
        return step.execute(driver)
    except Exception as e:
        print(e)
        notify_err_message(str(e))
        return False


def read_app_main_json(app_dir) -> dict:
    main_json_file = os.path.join(app_dir, "main.json")
    if not os.path.exists(main_json_file):
        return {}
    with open(main_json_file, 'r', encoding='utf8') as f:
        return json.load(f)


class WebAPP(object):

    def __init__(self, app_name="", username='', password='', **kwargs):
        self.app_name = app_name
        self.username = username
        self.password = password
        self.extra_data = kwargs
        self._steps = None
        web_app_dir = os.path.join(current_dir, 'apps', self.app_name)
        self._app_datas = read_app_main_json(web_app_dir)
        self._steps = sorted(self._app_datas.get("steps", self._default_custom_steps()), key=lambda item: item['step'])

    def _default_custom_steps(self) -> list:
        default_steps = [
            {
                "step": 1,
                "value": self.username,
                "target": self.extra_data.get('username_target', ''),
                "command": "type"
            },
            {
                "step": 2,
                "value": self.password,
                "target": self.extra_data.get('password_target', ''),
                "command": "type"
            },
            {
                "step": 3,
                "value": "",
                "target": self.extra_data.get('btn_target', ''),
                "command": "click"
            }
        ]
        return default_steps

    def execute(self, driver: webdriver.Chrome) -> bool:

        for step in self._steps:
            val = step['value']
            if val:
                val = val.replace("{USERNAME}", self.username)
                val = val.replace("{PASSWORD}", self.password)
                for k, v in self.extra_data.items():
                    val = val.replace('{%s}' % k.upper(), v)
            step['value'] = val
            action = StepAction(**step)
            ret = execute_action(driver, action)
            if not ret:
                unblock_input()
                notify_err_message("执行失败")
                block_input()
                return False
        return True


class WebChrome(object):

    def __init__(self, url='', **kwargs):
        self.driver = None
        self.url = url
        self.extra_data = kwargs
        self.app = WebAPP(**kwargs)

        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self._chrome_options.add_argument("start-maximized")
        self._chrome_options.add_argument("--disable-extensions")
        self._chrome_options.add_argument("--disable-dev-tools")

        # 禁用 密码管理器弹窗
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        self._chrome_options.add_experimental_option("prefs", prefs)

    def run(self):
        service = Service()
        #  driver 的 console 终端框不显示
        service.creationflags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(options=self._chrome_options, service=service)
        self.driver.implicitly_wait(10)
        if self.url != "":
            self.driver.get(self.url)
            ok = self.app.execute(self.driver)
            if not ok:
                notify_err_message("执行存在错误，退出")
                return
        self.driver.maximize_window()

    def wait_disconnected(self):
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

    def close(self):
        if self.driver:
            try:
                self.driver.close()
            except Exception as e:
                print(e)


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
    parser = argparse.ArgumentParser()
    parser.add_argument("base64_args", type=str, help="base64 args")
    parser.add_argument('-d', "--debug", help="debug mod", action='store_true', default=False)
    args = parser.parse_args()
    data = get_default_meta()
    data.update(parse_base64_str(args.base64_args))
    app = WebChrome(**data)
    block_input()
    app.run()
    unblock_input()
    app.wait_disconnected()
    app.close()
    if not args.debug:
        terminate_rdp_session()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
