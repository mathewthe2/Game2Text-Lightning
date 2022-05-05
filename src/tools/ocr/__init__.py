from tools import OCR_Engine, path_to_tesseract
from .tesseract import Tesseract

class OCR():
    def __init__(self, engine=OCR_Engine.TESSERACT_DEFAULT):
        self.engine = engine

    def get_boxed_characters(self, image, origin):
        if self.engine == OCR_Engine.TESSERACT_DEFAULT:
            tesseract = Tesseract(path_to_tesseract)
            return tesseract.extract_boxed_characters(image, origin)
        else:
            return []