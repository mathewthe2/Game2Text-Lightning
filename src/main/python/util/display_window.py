import sys
# from PyQt5.QtWidgets import QApplication
# from PyQt5 import QtCore
if sys.platform == 'win32':
    from ctypes import windll

class DisplayWindow():
    def __init__(self, width, height):
        if sys.platform == 'win32':
            screen_w = windll.user32.GetSystemMetrics(0)
            screen_h = windll.user32.GetSystemMetrics(1)
            original_width = screen_w
            original_height = screen_h
            windll.user32.SetProcessDPIAware()
            screen_w = windll.user32.GetSystemMetrics(0)
            screen_h = windll.user32.GetSystemMetrics(1)
            self.width_scale = screen_w//original_width
            self.height_scale = screen_h//original_height
            # QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
            self.width = width*self.width_scale
            self.height = height*self.height_scale
        else:
            self.width = width
            self.height = height
