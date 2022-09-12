# -*-coding=utf-8 -*-
import subprocess
import sys
import time
from subprocess import CREATE_NO_WINDOW

_blockInput = None

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
        return _blockInput(True)


def unblock_input():
    if _blockInput:
        return _blockInput(False)


def terminate_rdp_session():
    """
    执行 windows tsdiscon 命令 关闭当前远程会话
    :return:
    """
    subprocess.call(['tsdiscon'], creationflags=CREATE_NO_WINDOW)


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


def notify_err_message(msg):
    if _messageBox:
        _messageBox(msg, 'Error')


def wait_pid(pid):
    while 1:
        time.sleep(5)
        ok = check_pid_alive(pid)
        if not ok:
            notify_err_message("程序退出")
            break
