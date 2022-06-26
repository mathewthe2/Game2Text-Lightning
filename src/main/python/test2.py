import cv2
import numpy as np
import sys

import ctypes
import ctypes.wintypes
from ctypes.wintypes import HWND, RECT, DWORD
from ctypes import *

import win32gui
import win32con

from PIL import ImageGrab


# global variables
dwmapi = ctypes.WinDLL("dwmapi")
APP_NAME = ''
win_hwnd = -1

active = True


def callback(hwnd, extra):
    wnd_name = win32gui.GetWindowText(hwnd)

    if (wnd_name == APP_NAME):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        #print("Name: %s" % wnd_name)
        #print("\tLocation: (%d, %d)" % (x, y))
        #print("\t    Size: (%d, %d)" % (w, h))

        if (x >= 0 and y >= 0):
            global win_hwnd
            win_hwnd = hwnd


def windowGrab(window_title=None):
    global APP_NAME, win_hwnd
    APP_NAME = window_title

    if (window_title is None) or (len(window_title) == 0):
        print('!!! window_title == None')
        sys.exit(-1)

    # try to find a window with matching title and valid coordinates
    win32gui.EnumWindows(callback, None)

    # check if it has focus
    if (win_hwnd != win32gui.GetForegroundWindow()):
        print('not focused')
        win32gui.SetActiveWindow(win_hwnd)
        win32gui.SetForegroundWindow(win_hwnd)

hwnd_title = dict()
def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})

win32gui.EnumWindows(get_all_hwnd, 0)

for h,t in hwnd_title.items():
    if t is not "":
        # print(h, t)
        if 'persona.jpg' in t:
            windowGrab(t)

# main()
# windowGrab("Calculator")

# workaround to allow ImageGrab to capture the whole screen
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# get monitor resolution
screen_w = ctypes.windll.user32.GetSystemMetrics(0)
screen_h = ctypes.windll.user32.GetSystemMetrics(1)
print('screen_w=', screen_w, 'screen_h=', screen_h)

# loop
while active:
    # retrieve size and position of the window
    rect = RECT()
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    dwmapi.DwmGetWindowAttribute(HWND(win_hwnd), DWORD(DWMWA_EXTENDED_FRAME_BOUNDS), ctypes.byref(rect), ctypes.sizeof(rect))

    x = rect.left
    y = rect.top
    w = rect.right- x
    h = rect.bottom - y
    print('x=', x, 'y=', y, 'w=', w, 'h=', h)

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

    cv2.imshow('window', cropped_bgr)
    key = cv2.waitKey(0)
    # if (key & 0xFF) == ord('q'):
    #     break

    active = False

cv2.destroyAllWindows()