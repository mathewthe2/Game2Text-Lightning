from tools import STR_Engine
from .boxes import add_padding, combine_boxes
from .east_text_detector import East_Text_Detector

class STR():
    padding = 5

    def __init__(self, engine=STR_Engine.EAST):
        self.engine = engine

    # TODO: pass cursor coorindates to return closest box
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