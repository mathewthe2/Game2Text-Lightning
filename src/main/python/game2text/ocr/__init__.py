from .paddle_ocr import Paddle_OCR
from util.image import IMAGE_TYPE
from enum import Enum

# Optical Character Recognition Engine
class OCR_Engine(Enum):
    PADDLE_OCR = 1
    SPACE_OCR = 2
    GOOGLE_VISION = 3

ENGINE_PATHS = {
    OCR_Engine.PADDLE_OCR: "models/paddleocr"
}

class OCR():
    def __init__(self, appctxt, engine=OCR_Engine.PADDLE_OCR):
        self.engine = engine
        self.manga_ocr_engine = None
        self.paddle_engine = None
        self.path = appctxt.get_resource(ENGINE_PATHS[engine])

    # PIL image
    def get_text(self, image_object):
        if self.engine == OCR_Engine.PADDLE_OCR:
            if self.paddle_engine is None:
                self.paddle_engine = Paddle_OCR(self.path)
            return self.paddle_engine.extract_text(image_object.get_image(IMAGE_TYPE.NP))
        else:
            return []