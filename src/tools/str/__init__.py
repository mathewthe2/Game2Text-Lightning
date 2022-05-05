from tools import STR_Engine
from .boxes import add_padding, combine_boxes, point_distance_to_rect
from .east_text_detector import East_Text_Detector

class STR():
    padding = 5

    def __init__(self, engine=STR_Engine.EAST):
        self.engine = engine

    def get_cropped_images(self, image):
        if self.engine == STR_Engine.EAST:
            detector = East_Text_Detector(image)
            boxes = detector.detect()
            combined_boxes = combine_boxes(boxes)
            padded_boxes = add_padding(combined_boxes)
            cropped_images = [detector.crop(box) for box in padded_boxes]
            return cropped_images
        else:
            return []

    def get_closest_image(self, images, point):
        return min(images, key=lambda x:point_distance_to_rect(point, x.box()))