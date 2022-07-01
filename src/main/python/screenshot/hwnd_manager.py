import win32gui
import logging

class HWNDManager():
    hwnd_title = dict()

    def get_hwnd(self, title):
        win32gui.EnumWindows(self.get_all_hwnd, 0)
        print(self.hwnd_title)
        try:
            hwnd = next(hwnd for hwnd, value in self.hwnd_title.items() if value == title)
            return hwnd
        except:
            logging.error('hwnd of window not found')
            return None

    def get_hwnd_titles(self):
        win32gui.EnumWindows(self.get_all_hwnd, 0)
        return [t for t in self.hwnd_title.values() if t is not ""]

    def get_all_hwnd(self, hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
            
if __name__ == '__main__':
    m = HWNDManager()
    title = m.get_hwnd_titles()[0]
    print(title)
    print(m.get_hwnd(title))
