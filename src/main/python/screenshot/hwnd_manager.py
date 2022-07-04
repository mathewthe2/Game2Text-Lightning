import win32gui
from window_object import WindowObject

class HWNDManager():
    window_dict = dict()

    def get_window_objects(self):
        win32gui.EnumWindows(self.get_all_hwnd, 0)
        return self.window_dict.values()

    def get_all_hwnd(self, hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            self.window_dict.update({hwnd:WindowObject(hwnd)})

if __name__ == '__main__':
    m = HWNDManager()
    w = m.get_window_objects()
    print(',' .join([window.title for window in w]))
