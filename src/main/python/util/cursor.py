import platform

is_windows = (platform.system() == 'Windows')
if is_windows:
    from ctypes import windll, Structure, c_long, byref

# https://github.com/SkyleDc/PyQT-MouseCoFinder/blob/main/MouseCoFinder.py

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def cursor_position():
    if is_windows:
        mousecoords = POINT()
        windll.user32.GetCursorPos(byref(mousecoords))
        return mousecoords.x, mousecoords.y
