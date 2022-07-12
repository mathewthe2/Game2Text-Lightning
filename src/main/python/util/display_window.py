import sys
if sys.platform == 'win32':
    from ctypes import windll

REFERENCE_WIDTH = 1920
REFERENCE_HEGHT = 1080

class DisplayWindow():
    def __init__(self, width, height):
        if sys.platform == 'win32':
            windll.user32.SetProcessDPIAware()
            screen_w = windll.user32.GetSystemMetrics(0)
            screen_h = windll.user32.GetSystemMetrics(1)
            self.width = width * screen_w // REFERENCE_WIDTH
            self.height = height * screen_h // REFERENCE_HEGHT
        else:
            self.width = width
            self.height = height
