from BlurWindow.blurWindow import GlobalBlur
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QRegion
from PyQt5.QtCore import Qt

class BlurWindow(QtWidgets.QWidget):
    def __init__(self, x, y, w, h):
        super(BlurWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        )
        self.setGeometry(x, y, w, h)
        self.resize_fixed(w, h)

        # Rounded Corner
        radius = 20.0
        path = QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        
        # Blur
        GlobalBlur(self.winId(), Acrylic=False, Dark=False, QWidget=self)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0); border-radius: 20px")

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.3)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))   
        painter.drawRect(self.rect())

    def resize_fixed(self, w, h):
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.w = w
        self.h = h
    
    def resetGeometry(self, x, y, w, h):
        self.resize_fixed(w, h)
        self.move(x, y)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    grabber = BlurWindow(0, 0, 500, 500)
    # grabber = BlurWindow(1055, 603, 333, 106)
    grabber.show()
    sys.exit(app.exec_())