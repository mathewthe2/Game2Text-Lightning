from g2t_tools import OCR_Engine, paddle_models_path
from .paddle_ocr import Paddle_OCR
from util.image_object import IMAGE_TYPE

class OCR():
    def __init__(self, engine=OCR_Engine.PADDLE_OCR):
        self.engine = engine
        self.manga_ocr_engine = None
        self.paddle_engine = None

    # PIL image
    def get_text(self, image_object):
        if self.engine == OCR_Engine.PADDLE_OCR:
            if self.paddle_engine is None:
                self.paddle_engine = Paddle_OCR(paddle_models_path)
            return self.paddle_engine.extract_text(image_object.get_image(IMAGE_TYPE.NP))
        else:
            return []