class CroppedImage():
    def __init__(self, image, rW, rH, box):
        x, y, x2, y2 = box
        x = int(x * rW)
        y = int(y * rH)
        x2 = int(x2 * rW)
        y2 = int(y2 * rH)
        h = abs(y2-y)
        w = abs(x2-x)
        self.image = image[y:y + h, x:x + w]
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

    def get_image(self):
        return self.image

    def origin(self):
        return (self.x, self.y)

    def box(self):
        return (self.x, self.y, self.x2, self.y2)