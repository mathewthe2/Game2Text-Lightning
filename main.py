import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from CaptureScreen import CaptureScreen
from Overlay import Overlay
from mouse import querymouseposition
from result import Result
from tooltip import Tooltip

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200
IMG_FILE_NAME = 'temp.jpg'
result = Result([])
tooltip = None
  
class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.active_x = 500
        self.active_y = 500
        self.snippingWidget = CaptureScreen()
        self.snippingWidget.onSnippingCompleted = self.onSnippingCompleted
        self.overlay = Overlay()

        # set the title
        self.setWindowTitle("Snip")

        # set always on top
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        # setting  the geometry of window
        self.setGeometry(self.active_x, self.active_y, WINDOW_WIDTH, WINDOW_HEIGHT)

        pybutton = QtWidgets.QPushButton('Select', self)
        pybutton.resize(100,32)
        pybutton.move(50, 50) 
        pybutton.setDisabled(True)      
        pybutton.clicked.connect(self.clickMethod)

        closeButton = QtWidgets.QPushButton('Close', self)
        closeButton.resize(100,32)
        closeButton.move(50, 100)    
        closeButton.clicked.connect(self.closeAll) 

        self.show()

    def clickMethod(self):
        self.hide()
        self.snippingWidget.start()

    def closeAll(self):
        self.overlay.close()
        self.close()

    def onSnippingCompleted(self, data):
        self.show()
        self.setWindowState(QtCore.Qt.WindowState.WindowActive)
        # if grabbedPixMap is None:
        #     return 
        # grabbedPixMap.save(IMG_FILE_NAME, 'jpg')
        img, origin, end = data

        print('origin', origin)

        from test import show_image
        characters = show_image(img, origin, end)
        global result
        result = Result(characters)

        # self.overlay.start(origin, end)
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

    def closeEvent(self, event):
        global tooltip
        if tooltip:
            tooltip.close()

def update_coords():
    # print(querymouseposition())
    x, y = querymouseposition()
    r = result.detect_character((x, y))
    if r:
        y -= 300
        global tooltip
        if tooltip is None:
            tooltip = Tooltip(r[0].text, x, y)
            tooltip.show()
        else:
            tooltip.setWindowTitle(r[0].text)
            tooltip.updateLabel(r[0].text)
            tooltip.move(x, y)
        # t = Tooltip(r[0].text, x, y)
        # t.show()
        print(', '.join([c.text for c in r]))

def main():
    App = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.snippingWidget.start()
    # window.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(update_coords)
    timer.start(40)

    sys.exit(App.exec())

if __name__ == '__main__':
    main()