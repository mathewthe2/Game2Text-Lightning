import numpy as np

class ImageBox():

    def __init__(self, box, image, text=''):
        self.box = box
        self.image = image
        self.text = text

    def set_text(self, text):
        self.text = text

    def adjust_to_origin(self, origin):
        origin_x, origin_y = origin
        x1, y1, x2, y2 = self.box
        self.box =  x1 + origin_x, y1 + origin_y, x2 + origin_x, y2 + origin_y

    def touches_point(self, point):
        return pointInRect(point, self.rect())

    def width(self):
        x1, y1, x2, y2 = self.box
        return abs(x1 - x2)

    def height(self):
        x1, y1, x2, y2 = self.box
        return abs(y1 - y2)

    def rect(self):
        x1, y1, x2, y2 = self.box
        return x1, y1, self.width(), self.height()

    def is_similar(self, candidate_image):
        np_image = np.asarray(self.image)
        np_candidate =  np.asarray(candidate_image.image)
        return np_image.shape == np_candidate.shape and not(np.bitwise_xor(np_image,np_candidate).any())

def pointInRect(point,rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False