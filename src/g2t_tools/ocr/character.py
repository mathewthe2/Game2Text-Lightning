class Character():
    def __init__(self, text, x1 , x2, y1, y2, index=-1):
        self.text = text
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.index = index

    def touches_point(self, point):
        return pointInRect(point, self.rect())

    def width(self):
        return abs(self.x1 - self.x2)

    def height(self):
        return abs(self.y1 - self.y2)

    def rect(self):
        return self.x1, self.y1, self.width(), self.height()

def pointInRect(point,rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False