from g2t_tools.str.boxes import combine_boxes, rect_distance

class DetectionBox():
    def __init__(self, box, text_boxes):
        self.box = box
        self.text_boxes = text_boxes

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

    def add_padding(self, padding=5):
        x, y, x2, y2 = self.box
        self.box = (max(0, x-padding), max(0, y-padding), x2+padding, y2+padding)

def grouped_boxes(text_boxes, threshold=30, origin=0):
    combined_boxes = combine_boxes([text_box.box for text_box in text_boxes], threshold)
    detection_boxes = []
    for combined_box in combined_boxes:
        detection_box = DetectionBox(combined_box, [])
        detection_box.adjust_to_origin(origin)
        for text_box in text_boxes:
            if rect_distance(combined_box, text_box.box) == 0:
                detection_box.text_boxes.append(text_box)
        detection_box.add_padding()
        detection_boxes.append(detection_box)
    return detection_boxes

def pointInRect(point,rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False