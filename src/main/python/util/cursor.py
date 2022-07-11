import sys

if sys.platform == "win32":
    from ctypes import windll, Structure, c_long, byref
else:
    from pynput.mouse import Button, Controller
    mouse = Controller()

def cursor_position():
    if sys.platform == "win32":
        # https://github.com/SkyleDc/PyQT-MouseCoFinder/blob/main/MouseCoFinder.py
        class POINT(Structure):
            _fields_ = [("x", c_long), ("y", c_long)]
        mousecoords = POINT()
        windll.user32.GetCursorPos(byref(mousecoords))
        return mousecoords.x, mousecoords.y
    else:
        mouse = Controller()
        return mouse.position