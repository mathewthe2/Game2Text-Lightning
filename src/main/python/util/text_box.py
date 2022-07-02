class TextBox():
    def __init__(self, text, box):
        self.text = text
        self.box = box

    def width(self):
        x1, y1, x2, y2 = self.box
        return abs(x1 - x2)

    def height(self):
        x1, y1, x2, y2 = self.box
        return abs(y1 - y2)