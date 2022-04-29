# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ctypes import windll, Structure, c_long, byref

# https://github.com/SkyleDc/PyQT-MouseCoFinder/blob/main/MouseCoFinder.py

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def querymouseposition():
    mousecoords = POINT()
    windll.user32.GetCursorPos(byref(mousecoords))
    return mousecoords.x, mousecoords.y


# app = QApplication(sys.argv)
# Window = QWidget()
# Window.setWindowTitle('Mouse Coordinates Finder')
# Window.setWindowIcon(QIcon(':MouseCoFinder.ico'))

# Window.setFixedSize(250, 100)

# HorizontalLayout = QHBoxLayout(Window)

# Coords = QLabel(querymouseposition())
# Coords.setFont(QFont('Arial Black', 18))
# Coords.setAlignment(Qt.AlignCenter)

# HorizontalLayout.addWidget(Coords)


# def update_coords():
    # Coords.setText(querymouseposition())
    # print(querymouseposition())


# timer = QTimer()
# timer.timeout.connect(update_coords)
# timer.start(40)

# Window.show()

# sys.exit(app.exec_())