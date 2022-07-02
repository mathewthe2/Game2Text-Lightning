import sys
import ctypes
from ctypes.wintypes import HWND, RECT, DWORD
from ctypes import *
import win32gui
import cv2
from PIL import ImageGrab
import numpy as np
from util.image.image_object import ImageObject
from util.image import IMAGE_TYPE
from .hwnd_manager import HWNDManager
from game2text.capture_object import CaptureObject

dwmapi = ctypes.WinDLL("dwmapi")

class CaptureWindow():
    def __init__(self, window_title=''):
        self.win_hwnd = -1
        self.APP_NAME = window_title
        self.window_title = window_title
        self.hwnd_manager = HWNDManager()

    def setWindowTitle(self, window_title):
        self.window_title = window_title
        self.APP_NAME = window_title

    def windowGrab(self):
        if (self.window_title is None) or (len(self.window_title) == 0):
            print('!!! window_title == None')
            sys.exit(-1)
        # try to find a window with matching title and valid coordinates
        # win32gui.EnumWindows(self.callback, None)
        self.win_hwnd = self.hwnd_manager.get_hwnd(self.window_title)

        # check if it has focus
        # if (self.win_hwnd and self.win_hwnd != win32gui.GetForegroundWindow()):
        #     print('not focused')
        #     win32gui.SetActiveWindow(self.win_hwnd)
        #     win32gui.SetForegroundWindow(self.win_hwnd)

    def callback(self, hwnd, extra):
        wnd_name = win32gui.GetWindowText(hwnd)

        if (wnd_name == self.APP_NAME):
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y

            # print("Name: %s" % wnd_name)
            # print("\tLocation: (%d, %d)" % (x, y))
            # print("\t    Size: (%d, %d)" % (w, h))

            if (x >= 0 and y >= 0):
                self.win_hwnd = hwnd
        # print('result', self.win_hwnd)

    def show_capture(self):
        image = self.get_capture()
        cv2.imshow('window', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # https://stackoverflow.com/questions/60067002/problems-while-taking-screenshots-of-a-window-and-displaying-it-with-opencv
    def get_capture(self):
        self.windowGrab()
        if not self.win_hwnd:
            return None

        # workaround to allow ImageGrab to capture the whole screen
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()

        # get monitor resolution
        screen_w = ctypes.windll.user32.GetSystemMetrics(0)
        screen_h = ctypes.windll.user32.GetSystemMetrics(1)
        print('screen_w=', screen_w, 'screen_h=', screen_h)

        origin = ()
        end = ()
        # TODO: timeout to exit while loop
        active = True
        while active:
            # retrieve size and position of the window
            rect = RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            dwmapi.DwmGetWindowAttribute(HWND(self.win_hwnd), DWORD(DWMWA_EXTENDED_FRAME_BOUNDS), ctypes.byref(rect), ctypes.sizeof(rect))
            x = rect.left
            y = rect.top
            w = rect.right- x
            h = rect.bottom - y
            print('x=', x, 'y=', y, 'w=', w, 'h=', h)
            origin = (x, y)
            end = (rect.right, rect.bottom)
            if (w == 0 or h == 0):
                continue
            # take a full screenshot of the desktop
            full_screen = np.array(ImageGrab.grab( bbox= (0, 0, screen_w, screen_h) ))
            if (full_screen is None):
                continue
            # crop window area from the screenshot
            cropped_rgb = full_screen[y : y+h, x : x+w]
            # convert from RGB to BGR order so that colors are displayed correctly
            cropped_bgr = cv2.cvtColor(cropped_rgb, cv2.COLOR_RGB2BGR)
            active = False
            
        image_object = ImageObject(cropped_bgr, IMAGE_TYPE.CV)
        capture_object = CaptureObject(image_object, origin, end)
        return capture_object



hw = dict()
def get_all_hwnd(self, hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hw.update({hwnd:win32gui.GetWindowText(hwnd)})

if __name__ == '__main__':
    hw = dict()
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hw.update({hwnd:win32gui.GetWindowText(hwnd)})
    win32gui.EnumWindows(get_all_hwnd, 0)
    hwnd_title = ''
    for h,t in hw.items():
        if t is not "":
            if 'persona.jpg' in t:
                hwnd_title = t
    print(hwnd_title)
    cw = CaptureWindow(hwnd_title)
    cw.show_capture()
