import sys

if sys.platform == 'win32':
    from pywinauto import Application
    from pywinauto.controls.uia_controls import (ButtonWrapper, EditWrapper, MenuItemWrapper,
                                                 MenuWrapper, ComboBoxWrapper, ToolbarWrapper)
#   process = subprocess.Popen([prog_path, ],
#                                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
#   process.wait()
from common import (BaseApplication, wait_pid, )


class AppletApplication(BaseApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = self.manifest.path
        self.username = self.account.username
        self.password = self.account.secret
        self.host = self.asset.address
        self.port = self.asset.get_protocol_port(self.protocol)
        self.db = self.asset.category_property.db_name
        self.pid = None

    def run(self):
        app = Application(backend='uia')
        app.start(self.path)
        app.Dialog.wait('ready', )
        self.pid = app.process
        if not all([self.username, self.password, self.host]):
            print(f'缺少必要的参数')
            return
        url = "{}:{}/{}".format(self.host, self.port, self.db)
        app.Dialog.Edit1.set_text(self.password)
        app.Dialog.Edit2.set_text(self.username)
        app.Dialog.Edit3.set_text(url)
        app.Dialog.Button4.click()

    def wait(self):
        wait_pid(self.pid)
