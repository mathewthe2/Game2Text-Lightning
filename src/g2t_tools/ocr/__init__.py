from g2t_tools import OCR_Engine, paddle_models_path
# from .tesseract import Tesseract
# from .manga_ocr import Manga_OCR
from .paddle_ocr import Paddle_OCR
from util.image_object import IMAGE_TYPE

class OCR():
    def __init__(self, engine=OCR_Engine.PADDLE_OCR):
        self.engine = engine
        self.manga_ocr_engine = None
        self.paddle_engine = None

    # PIL image
    def get_text(self, image_object):
        # if self.engine == OCR_Engine.MANGA_OCR:
        #     if self.manga_ocr_engine is None:
        #         self.manga_ocr_engine = Manga_OCR(manga_ocr_path)
        #     return self.manga_ocr_engine.extract_text(image)
        # elif self.engine == OCR_Engine.TESSERACT:
        #     teseract_engine = Tesseract(path_to_tesseract) 
        #     return teseract_engine.extract_text(image)
        if self.engine == OCR_Engine.PADDLE_OCR:
            if self.paddle_engine is None:
                self.paddle_engine = Paddle_OCR(paddle_models_path)
            return self.paddle_engine.extract_text(image_object.get_image(IMAGE_TYPE.NP))
        else:
            return []