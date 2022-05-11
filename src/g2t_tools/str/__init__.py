from torch import xlogy_
from g2t_tools import STR_Engine, paddle_models_path
from image_box import ImageBox
from util.image_object import IMAGE_TYPE
from .boxes import add_padding, combine_boxes, point_distance_to_rect
from .east_text_detector import East_Text_Detector
from .paddle_detector import Paddle_Detector

class STR():
    padding = 5

    def __init__(self, engine=STR_Engine.PADDLE, is_combine_neighbors=False, combine_threshold=15):
        self.engine = engine
        self.paddle_engine = Paddle_Detector(paddle_models_path)
        self.is_combine_neighbors = is_combine_neighbors
        self.combine_threshold = combine_threshold

    #  input image pil, output list of image pils
    def get_cropped_image_boxes(self, image_object):
        if self.engine == STR_Engine.PADDLE:
            boxes = self.paddle_engine.detect(image_object.get_image(IMAGE_TYPE.NP))
            if self.is_combine_neighbors:
                boxes = combine_boxes(boxes, self.combine_threshold)
            if self.padding > 0:
                boxes = add_padding(boxes, self.padding)
            image = image_object.get_image(IMAGE_TYPE.PIL)
            image_boxes = [ImageBox(box, image.crop(box)) for box in boxes]
            return image_boxes
        # elif self.engine == STR_Engine.EAST:
        #     detector = East_Text_Detector(image_object.get_image(IMAGE_TYPE.CV))
        #     boxes = detector.detect()
        #     combined_boxes = combine_boxes(boxes)
        #     padded_boxes = add_padding(combined_boxes)
        #     cropped_images = [detector.crop(box) for box in padded_boxes]
        #     return cropped_images
        else:
            return []

    # def get_closest_image(self, images, point):
    #     return min(images, key=lambda x:point_distance_to_rect(point, x.box()))

    def get_closest_image(self, image_boxes, point):
        return min(image_boxes, key=lambda image_box:point_distance_to_rect(point, image_box.box))