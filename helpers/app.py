from pywinauto.application import Application, WindowSpecification


# 通过进程ID获取应用程序的句柄
def get_app_by_process_id(pid):
    return Application().connect(process=pid)


# 获取当前 应用的所有窗口
def list_app_windows(app: Application):
    return app.windows()


# 最小化 minimize()
def minimize_app_windows(app: Application):
    for window in app.windows():
        window.minimize()


# 最大化 maximize()
def maximize_app_windows(app: Application, win_spec: WindowSpecification):
    win_spec.restore().set_focus()
