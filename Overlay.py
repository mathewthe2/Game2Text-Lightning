from PyQt5 import QtWidgets, QtCore

# screen_width = 200
# screen_height = 100

class Overlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.screen_width = None
        self.screen_height = None
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

    def start(self, origin, end):
        x, y, w, h = self.box_from_two_points(origin, end)
        self.setGeometry(x, y, w, h)
        self.show()

    def box_from_two_points(self, origin, end):
        x = min(origin.x(), end.x())
        y = min(origin.y(), end.y())
        x2 = max(origin.x(), end.x())
        y2 = max(origin.y(), end.y())
        w = abs(x-x2)
        h = abs(y-y2)
        return x, y, w, h
