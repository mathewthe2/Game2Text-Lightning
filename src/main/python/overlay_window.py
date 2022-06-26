from BlurWindow.blurWindow import GlobalBlur
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
import sys
from util.label import Label
from util.font import get_font_size
from japanese import initLanguage

class OverlayWindow(QtWidgets.QWidget):
    def __init__(self, textContent, x, y, w=800, h=300):
        super(OverlayWindow, self).__init__()
        self.translator = initLanguage()
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        )
        self.setGeometry(x, y, w, h)
        self.resize_fixed(w, h)
        # self.resize(500, 400)

        GlobalBlur(self.winId(), Acrylic=False, Dark=False, QWidget=self)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

        self.h_box = QtWidgets.QHBoxLayout(self)
        self.setText(textContent)
            
        # label = createLabel(s)
        # h_box.addWidget(label)
        self.h_box.setSpacing(0)
        self.h_box.setContentsMargins(0, 0, 0, 0)
        self.h_box.setAlignment(QtCore.Qt.AlignLeft)

    def resize_fixed(self, w, h):
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.w = w
        self.h = h

    def setText(self, textContent):
        font_size = get_font_size(textContent, 'Times', self.w, self.h)
        for i in range(0, len(textContent)):
            label = self.createLabel(textContent[i:], font_size)
            self.h_box.addWidget(label)

    def updateText(self, textContent):
        self.clearLayout(self.h_box)
        self.setText(textContent)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    
    def createLabel(self, text, font_size):
        label = Label(text, self.translator)
        font = QFont('Times', font_size)
        label.setFont(font)
        label.setStyleSheet("QLabel { color : coral; }")
        # label.setStyleSheet("border-style:solid; color: black; border-width: 1px")
        label.setAlignment(QtCore.Qt.AlignLeft)
        # label.setContentsMargins(0, 0, 0, 0)
        return label




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = OverlayWindow('家のお使いだったから', 500, 500, 350, 30)
    mw.show()
    sys.exit(app.exec())