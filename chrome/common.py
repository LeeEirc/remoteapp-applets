import sys

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
