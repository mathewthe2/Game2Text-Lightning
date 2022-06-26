from PyQt5.QtWidgets import QLabel

class Label(QLabel):
    def __init__(self, text, translator):
        QLabel.__init__(self, text[0]) # only show first character
        self.full_text = text
        self.translator = translator

    def enterEvent(self, event):
        print(self.full_text)
        print(self.translator.findTerm(self.full_text))

    def leaveEvent(self, event):
        pass
        # print("left")