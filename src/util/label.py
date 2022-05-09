from PyQt5.QtWidgets import QLabel

class Label(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)

    def enterEvent(self, event):
        print(self.text())

    def leaveEvent(self, event):
        pass
        # print("left")