from BlurWindow.blurWindow import GlobalBlur
from PyQt5 import QtCore, QtWidgets

class BlurWindow(QtWidgets.QWidget):
    def __init__(self, x, y, w, h):
        super(BlurWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        )
        self.setGeometry(x, y, w, h)
        self.resize_fixed(w, h)

        GlobalBlur(self.winId(), Acrylic=False, Dark=False, QWidget=self)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

    def resize_fixed(self, w, h):
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.w = w
        self.h = h
    
    def resetGeometry(self, x, y, w, h):
        self.move(x, y)
        self.resize_fixed(w, h)


# if __name__ == '__main__':
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     grabber = BlurWindow(500, 500, 500, 500)
#     grabber = BlurWindow(1055, 603, 333, 106)
#     grabber.show()
#     sys.exit(app.exec_())