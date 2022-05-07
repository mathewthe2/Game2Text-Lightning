from manga_ocr import MangaOcr
import cv2
from PIL import Image

class Manga_OCR():
    def __init__(self, model_path):
        self.mocr = MangaOcr(pretrained_model_name_or_path=model_path)

    def extract_text(self, image):
        text = self.mocr(image)
        return text
