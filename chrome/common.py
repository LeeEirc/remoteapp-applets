import abc
import subprocess
import sys
import time
import os
import json
import base64
from subprocess import CREATE_NO_WINDOW

current_dir = os.path.dirname(__file__)

_blockInput = None
_messageBox = None
if sys.platform == 'win32':
    import ctypes
    from ctypes import wintypes
    import win32ui

    # import win32con

    _messageBox = win32ui.MessageBox

    _blockInput = ctypes.windll.user32.BlockInput
    _blockInput.argtypes = [wintypes.BOOL]
    _blockInput.restype = wintypes.BOOL


def block_input():
    if _blockInput:
        _blockInput(True)


def unblock_input():
    if _blockInput:
        _blockInput(False)


def notify_err_message(msg):
    if _messageBox:
        _messageBox(msg, 'Error')


def check_pid_alive(pid) -> bool:
    # tasklist  /fi "PID eq 508" /fo csv
    # '"映像名称","PID","会话名      ","会话#   ","内存使用 "\r\n"wininit.exe","508","Services","0","6,920 K"\r\n'
    try:

        csv_ret = subprocess.check_output(["tasklist", "/fi", f'PID eq {pid}', "/fo", "csv"],
                                          creationflags=CREATE_NO_WINDOW)
        content = csv_ret.decode()
        content_list = content.strip().split("\r\n")
        if len(content_list) != 2:
            notify_err_message(content)
            return False
        ret_pid = content_list[1].split(",")[1].strip('"')
        return str(pid) == ret_pid
    except Exception as e:
        notify_err_message(e)
        return False


def wait_pid(pid):
    while 1:
        time.sleep(5)
        ok = check_pid_alive(pid)
        if not ok:
            notify_err_message("程序退出")
            break


class DictObj:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)


class User(DictObj):
    id: str
    name: str
    username: str


class CategoryProperty(DictObj):
    autofill: str
    username_selector: str
    password_selector: str
    submit_selector: str
    script: list


class Category(DictObj):
    value: str
    label: str


class Asset(DictObj):
    id: str
    name: str
    address: str
    protocols: list
    category: Category
    category_property: CategoryProperty


class Account(DictObj):
    id: str
    name: str
    username: str
    secret: str


class Platform(DictObj):
    charset: str


class Manifest(DictObj):
    name: str
    version: str
    protocols: list[str]
    type: str


def get_manifest_data() -> dict:
    manifest_file = os.path.join(current_dir, 'manifests.json')
    try:
        with open(manifest_file, "r", encoding='utf8') as f:
            return json.load(f)
    except Exception as e:
        print(e)
    return {}


def convert_base64_to_json(base64_str: str) -> dict:
    try:
        data_json = base64.decodebytes(base64_str.encode('utf-8')).decode('utf-8')
        return json.loads(data_json)
    except Exception as e:
        print(e)
    return {}


class BaseApplication(abc.ABC):

    def __init__(self, user: User = None, asset: Asset = None, account: Account = None, platform: Platform = None,
                 **kwargs):
        self.user = user
        self.asset = asset
        self.account = account
        self.platform = platform

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError('run')

    @abc.abstractmethod
    def wait(self):
        raise NotImplementedError('wait')
