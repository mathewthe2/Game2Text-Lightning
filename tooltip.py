import sys
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QApplication, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot, Qt

class Tooltip(QMainWindow):
    # app = QApplication(sys.argv)
    # widget = QWidget()

    def __init__(self, text, x, y, w=320, h=200):
        super().__init__()
        # textLabel = QLabel(QWidget())
        # textLabel.setText(text)

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)  

        self.title = QLabel(text, self) 
        self.title.setAlignment(Qt.AlignCenter) 
        self.title.setFont(QFont('Times', 30))
        gridLayout.addWidget(self.title, 0, 0)

        self.setWindowTitle(text)
        self.setGeometry(x, y, w, h)
    
    def updateLabel(self, text):
        self.title.setText(text)
    

    # def __init__(self, text, x, y, w=320, h=200):
    #     textLabel = QLabel(QWidget())
    #     textLabel.setText(text)
    #     textLabel.move(110,85)

    #     self.setGeometry(x, y, w, h)
    #     self.setWindowTitle("PyQt5 Example")