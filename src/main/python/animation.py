import sys
from PyQt5.Qt import *


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: green;")
        self.resize(400, 400)
        
        self.label = QLabel()
        self.pixmap = QPixmap('Ok.png')
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background: #CD113B;")
        
        self.b = QPushButton("Reduce", self, clicked=self.reduce)
        self.b.setStyleSheet("background: blue; color: yellow;")
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.b)

    def reduce(self):
        self.anim = QPropertyAnimation(self, b"opacity")
        self.anim.setDuration(3000)        
        self.anim.setLoopCount(3)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)        
        self.anim.start()
            
    def windowOpacity(self):
        return super().windowOpacity()    
    
    def setWindowOpacity(self, opacity):
        super().setWindowOpacity(opacity)    
    
    opacity = pyqtProperty(float, windowOpacity, setWindowOpacity)    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Test()
    w.show()
    sys.exit(app.exec_())