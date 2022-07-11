from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication
import numpy as np
import cv2
from PIL import ImageGrab
from .MacCapture import cartesian_capture
from util.image.image_object import ImageObject
from game2text.capture_object import CaptureObject
from util.image import IMAGE_TYPE

IMG_FILE_NAME = 'temp.png'

# Refer to https://github.com/harupy/snipping-tool
class MacSnipper(QtWidgets.QWidget):
    is_snipping = False

    def __init__(self, parent=None, app=QApplication.instance()):
        super(MacSnipper, self).__init__()
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.screen = app.primaryScreen()
        self.setGeometry(0, 0, self.screen.size().width(), self.screen.size().height())
        self.origin = QtCore.QPoint()
        self.end =QtCore.QPoint()
        self.onSnippingCompleted = None

    def fullscreen(self):
        img = ImageGrab.grab(bbox=(0, 0, self.screen.size().width(), self.screen.size().height()))

        try:
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        except:
            img = None
            
        if self.onSnippingCompleted is not None:
            self.onSnippingCompleted(img)

    def start(self):
        MacSnipper.is_snipping = True
        self.setWindowOpacity(0.3)
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        if MacSnipper.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            self.origin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp =  QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRect(self.origin, self.end)
        qp.drawRect(rect)

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.end = self.origin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        MacSnipper.is_snipping = False
        QApplication.restoreOverrideCursor()
        x1 = min(self.origin.x(), self.end.x())
        y1 = min(self.origin.y(), self.end.y())
        x2 = max(self.origin.x(), self.end.x())
        y2 = max(self.origin.y(), self.end.y())

        self.repaint()
        QApplication.processEvents()

        screenShape = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        print(screenShape.width())
        print(screenShape.height())
        print('capturing')
        cartesian_capture(x=x1, 
                        y=y1, 
                        width=abs(x1-x2), 
                        height=abs(y1-y2), 
                        total_width = screenShape.width(),
                        total_height = screenShape.height(),
                        path=IMG_FILE_NAME)
        # img = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        # try:
        #     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # except:
        img = cv2.imread(IMG_FILE_NAME)
        image_object = ImageObject(img, IMAGE_TYPE.CV)
        capture_object = CaptureObject(image_object, (x1, y1), (x2, y2))
            
        if self.onSnippingCompleted is not None:
            self.onSnippingCompleted(capture_object)

        self.close()

    def captureArea(self, box=None):
        if box:
            x1, y1, x2, y2 = box
        else:
            x1 = self.origin.x()
            y1 = self.origin.y()
            x2 = self.end.x()
            y2 = self.end.y()
        screenShape = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        cartesian_capture(x=x1, 
                y=y1, 
                width=abs(x1-x2), 
                height=abs(y1-y2), 
                total_width = screenShape.width(),
                total_height = screenShape.height(),
                path=IMG_FILE_NAME)

        img = cv2.imread(IMG_FILE_NAME)
        image_object = ImageObject(img, IMAGE_TYPE.CV)
        capture_object = CaptureObject(image_object, (x1, y1), (x2, y2))
        return capture_object

# def main():
#     App = QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(App.exec())

# if __name__ == '__main__':
#     main()