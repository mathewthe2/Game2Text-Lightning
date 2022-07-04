import win32gui

class WindowObject():
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.title = win32gui.GetWindowText(hwnd)
        self.class_name = win32gui.GetClassName(hwnd)

    def is_same(self, window_object):
        return self.hwnd == window_object.hwnd or (self.title == window_object.title and self.class_name == window_object.class_name)
