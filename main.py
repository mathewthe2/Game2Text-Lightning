import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from SnippingWidget import SnippingWidget

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
IMG_FILE_NAME = 'temp.png'
  
class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.active_x = 120
        self.active_y = 120
        self.snippingWidget = SnippingWidget(app=QtWidgets.QApplication.instance())
        self.snippingWidget.onSnippingCompleted = self.onSnippingCompleted
  
        # set the title
        self.setWindowTitle("Snip")

        # set always on top
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        # setting  the geometry of window
        self.setGeometry(self.active_x, self.active_y, WINDOW_WIDTH, WINDOW_HEIGHT)

        pybutton = QtWidgets.QPushButton('Select', self)
        pybutton.resize(100,32)
        pybutton.move(100, 100)        
        pybutton.clicked.connect(self.clickMethod)

        self.show()

    def clickMethod(self):
        self.hide()
        self.snippingWidget.start() 

    def onSnippingCompleted(self, frame):
        self.show()
        self.setWindowState(QtCore.Qt.WindowState.WindowActive)
        if frame is None:
            return 

        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format.Format_RGB888)
        image.save(IMG_FILE_NAME)
        # pixmap = QPixmap.fromImage(image)
        # self._pixmap = self.resizeImage(pixmap)
        # self.ui.label.setPixmap(self._pixmap)

    def resizeImage(self, pixmap):
        lwidth = self.ui.label.width()
        pwidth = pixmap.width()
        lheight = self.ui.label.height()
        pheight = pixmap.height()

        wratio = pwidth * 1.0 / lwidth
        hratio = pheight * 1.0 / lheight

        if pwidth > lwidth or pheight > lheight:
            if wratio > hratio:
                lheight = pheight / wratio
            else:
                lwidth = pwidth / hratio

            scaled_pixmap = pixmap.scaled(lwidth, lheight)
            return scaled_pixmap
        else:
            return pixmap

    def moveEvent(self, event):    # QMoveEvent      
        self.active_x = event.pos().x()
        self.active_y = event.pos().y()
        super(Window, self).moveEvent(event)

def main():
    App = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())

if __name__ == '__main__':
    main()