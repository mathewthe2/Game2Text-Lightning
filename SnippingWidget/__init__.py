from PyQt6 import QtWidgets, QtCore, QtGui
import numpy as np
import cv2
from PIL import ImageGrab
import platform
platform_name = platform.system()
isMac = platform_name == 'Darwin'
if isMac:
    from MacCapture import cartesian_capture

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
IMG_FILE_NAME = 'temp.png'

# Refer to https://github.com/harupy/snipping-tool
class SnippingWidget(QtWidgets.QWidget):
    is_snipping = False

    def __init__(self, parent=None, app=None):
        super().__init__()
        screen_width = app.primaryScreen().size().width()
        screen_height = app.primaryScreen().size().height()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

    def start(self):
        SnippingWidget.is_snipping = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        SnippingWidget.is_snipping = False
        QtWidgets.QApplication.restoreOverrideCursor()
        self.close()

        if isMac:
            screenShape = QtGui.QGuiApplication.primaryScreen().availableGeometry()
            cartesian_capture(x=x1, 
                            y=y1, 
                            width=abs(x1-x2), 
                            height=abs(y1-y2), 
                            total_width = screenShape.width(),
                            total_height = screenShape.height(),
                            path=IMG_FILE_NAME)
            img = None
        else:
            x1 = min(self.begin.x(), self.end.x())
            y1 = min(self.begin.y(), self.end.y())
            x2 = max(self.begin.x(), self.end.x())
            y2 = max(self.begin.y(), self.end.y())
            

            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            img.save(IMG_FILE_NAME)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        
        cv2.imshow('Captured Image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if self.onSnippingCompleted is not None:
            self.onSnippingCompleted(img)
        self.close()