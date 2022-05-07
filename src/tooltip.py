import sys
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QApplication, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot, Qt

class Tooltip(QMainWindow):
    # app = QApplication(sys.argv)
    # widget = QWidget()

    def __init__(self, text, x, y, w=800, h=300):
        super().__init__()

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(self)     
        gridLayout.setContentsMargins(0, 0, 0, 0)
        centralWidget.setLayout(gridLayout) 

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint) 
        # self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.title = QLabel(text, self) 
        self.title.setAlignment(Qt.AlignVCenter) 
        font = QFont('Times', 15)
        # font.setPixelSize(self.height() * 0.8)
        self.title.setFont(font)
        self.title.setWordWrap(True)
        # self.title.setFixedWidth(500)
        gridLayout.addWidget(self.title, 0, 0)

        # self.setWindowTitle(text)
        self.setGeometry(x, y, w, h)
    
    def updateLabel(self, text):
        self.title.setText(text)
    

    # def __init__(self, text, x, y, w=320, h=200):
    #     textLabel = QLabel(QWidget())
    #     textLabel.setText(text)
    #     textLabel.move(110,85)

    #     self.setGeometry(x, y, w, h)
    #     self.setWindowTitle("PyQt5 Example")