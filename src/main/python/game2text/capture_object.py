from re import X
from util.image import IMAGE_TYPE
from util.image.image_box import ImageBox

class CaptureObject():
    def __init__(self, image_object, origin, end):
        self.image_object = image_object
        self.origin = origin
        self.end = end
    
    def get_image(self, type=IMAGE_TYPE.PIL):
        return self.image_object.get_image(type)

    def get_image_box(self):
        x1, y1 = self.origin
        x2, y2 = self.end
        box = x1, y1, x2, y2
        return ImageBox(box, self.get_image())

    def is_similar(self, other_capture_object):
        image_box = self.get_image_box()
        other_image_box = other_capture_object.get_image_box()
        return image_box.is_similar(other_image_box)

    def get_origin_point(self):
        x, y = self.origin
        return Point(x, y)

    def get_end_point(self):
        x, y = self.end
        return Point(x, y)

    def get_region_info(self):
        x, y = self.origin
        x2, y2 = self.end
        w = x2-x
        h = y2-y
        return 'Selected Region:({},{}) w:{} h:{}'.format(x, y, w, h)

    def is_valid(self):
        x, y = self.origin
        x2, y2 = self.end 
        return x < x2 and y < y2

class Point():
    def __init__(self, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
    
    def x(self):
        return self.x_cord

    def y(self):
        return self.y_cord