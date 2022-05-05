from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
import cv2
from PIL import ImageGrab
import platform
platform_name = platform.system()
isMac = platform_name == 'Darwin'
if isMac:
    from MacCapture import cartesian_capture
else:
    import tkinter as tk

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
IMG_FILE_NAME = 'temp.png'

# Refer to https://github.com/harupy/snipping-tool
class SnippingWidget(QtWidgets.QWidget):
    is_snipping = False
    background = True

    def __init__(self, parent=None, app=None):
        super().__init__()
        if isMac:
            screen_width = app.primaryScreen().size().width()
            screen_height = app.primaryScreen().size().height()
        else:
            root = tk.Tk()
            screen_width = root.winfo_screenwidth()
            screen_height= root.winfo_screenheight()

        print("screen_width", screen_width)
        print("screen_height", screen_height)
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

    def start(self):
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        SnippingWidget.background = False
        SnippingWidget.is_snipping = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        self.show()

    # def start(self):
    #     self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    #     SnippingWidget.is_snipping = True
    #     self.setWindowOpacity(0.3)
    #     QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
    #     self.show()

    def paintEvent(self, event):
        if SnippingWidget.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            # reset points, so the rectangle won't show up again.
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRect(self.begin, self.end)
        qp.drawRect(rect)

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
        # self.close()

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

            self.repaint()
            QtWidgets.QApplication.processEvents()
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))

            img.save(IMG_FILE_NAME)
            QtWidgets.QApplication.processEvents()

            img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        
        # cv2.imshow('Captured Image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if self.onSnippingCompleted is not None:
            self.onSnippingCompleted(img)
        self.close()
    
    def convert_numpy_img_to_qpixmap(self, np_img):
        height, width, channel = np_img.shape
        bytesPerLine = 3 * width
        return QtGui.QPixmap(QtGui.QImage(np_img.data, width, height, bytesPerLine, QtGui.QImage.Format.Format_RGB888).rgbSwapped())