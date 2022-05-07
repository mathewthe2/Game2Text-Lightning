from g2t_tools import OCR_Engine, path_to_tesseract, manga_ocr_path
from .tesseract import Tesseract
from .manga_ocr import Manga_OCR

class OCR():
    def __init__(self, engine=OCR_Engine.MANGA_OCR):
        self.engine = engine
        self.manga_ocr_engine = Manga_OCR(manga_ocr_path)

    # input PIL image
    def get_text(self, image):
        if self.engine == OCR_Engine.MANGA_OCR:
            return self.manga_ocr_engine.extract_text(image)
        elif self.engine == OCR_Engine.PADDLE_OCR:
            pass
        else:
            return []