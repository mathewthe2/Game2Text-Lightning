import win32gui

class HWNDManager():
    hwnd_title = dict()

    def get_hwnd_titles(self):
        win32gui.EnumWindows(self.get_all_hwnd, 0)
        return [t for t in self.hwnd_title.values() if t is not ""]

    def get_all_hwnd(self, hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
