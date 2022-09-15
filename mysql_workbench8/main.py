# -*-coding=utf-8 -*-
import base64
import json
import os.path
import sys

if sys.platform == 'win32':
    from pywinauto import Application
    from pywinauto.controls.uia_controls import (ButtonWrapper, EditWrapper, MenuItemWrapper,
                                                 MenuWrapper, ComboBoxWrapper, ToolbarWrapper)
from common import \
    (block_input, unblock_input, terminate_rdp_session, wait_pid, )

_default_path = r"C:\Program Files\MySQL\MySQL Workbench 8.0 CE\MySQLWorkbench.exe"

current_dir = os.path.dirname(__file__)
meta_file = os.path.join(current_dir, 'manifests.json')
meta_data = {
    'path': _default_path,
    'type': 'python',
    'protocols': ['mysql'],
}


class MySQLWorkBench8(object):

    def __init__(self, path=_default_path, username="", password='',
                 host='', port='', db_name='', **kwargs):
        self.path = path
        if not self.path:
            self.path = _default_path
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db = db_name
        self.pid = None

    def run(self):
        app = Application(backend='uia')
        app.start(self.path)
        self.pid = app.process
        if not any([self.username, self.password, self.host]):
            print(f'缺少必要的参数')
            return

        menubar = app.window(title="MySQL Workbench", auto_id="MainForm", control_type="Window") \
            .child_window(title="Database", control_type="MenuItem")
        menubar.wait('ready', timeout=10, retry_interval=5)
        MenuItemWrapper(menubar.element_info).select()
        cdb = menubar.child_window(title="Connect to Database", control_type="MenuItem")
        cdb.wait('ready', timeout=10, retry_interval=5)
        MenuItemWrapper(cdb.element_info).click_input()

        # 输入 host
        host_ele = app.top_window().child_window(title="Host Name", auto_id="Host Name", control_type="Edit")
        EditWrapper(host_ele.element_info).set_edit_text(self.host)

        # 输入 port
        port_ele = app.top_window().child_window(title="Port", auto_id="Port", control_type="Edit")
        EditWrapper(port_ele.element_info).set_edit_text(self.port)

        # 输入 username
        user_ele = app.top_window().child_window(title="User Name", auto_id="User Name", control_type="Edit")
        EditWrapper(user_ele.element_info).set_edit_text(self.username)

        # 输入 db
        db_ele = app.top_window().child_window(title="Default Schema", auto_id="Default Schema", control_type="Edit")
        EditWrapper(db_ele.element_info).set_edit_text(self.db)

        ok_ele = app.top_window().child_window(title="Connection", auto_id="Connection", control_type="Window") \
            .child_window(title="OK", control_type="Button")
        ButtonWrapper(ok_ele.element_info).click()

        # 输入 password
        password_ele = app.top_window().child_window(title="Password", auto_id="Password", control_type="Edit")
        password_ele.wait('ready', timeout=10, retry_interval=5)
        EditWrapper(password_ele.element_info).set_edit_text(self.password)

        ok_ele = app.top_window().child_window(title="Button Bar", auto_id="Button Bar", control_type="Pane") \
            .child_window(title="OK", control_type="Button")
        ButtonWrapper(ok_ele.element_info).click()


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
    app = MySQLWorkBench8(**data)
    block_input()
    app.run()
    unblock_input()
    wait_pid(app.pid)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    terminate_rdp_session()
