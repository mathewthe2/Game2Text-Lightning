from paddleocr import PaddleOCR
from pathlib import Path
import numpy as np

class Paddle_Detector():
    ocr = None
    image = None

    def __init__(self, models_path, padding=5):
        self.padding = padding
        self.load_model(models_path)

    def load_model(self, models_path):
        det_model_dir = str(Path(models_path, "whl", "det", "en", "en_ppocr_mobile_v2.0_det_infer"))
        rect_model_dir = str(Path(models_path, "whl", "rect", "japan", "japan_mobile_v2.0_rec_infer"))
        cls_model_dir = str(Path(models_path, "whl", "cls", "ch_ppocr_mobile_v2.0_cls_infer"))
        self.ocr = PaddleOCR(use_angle_cls=True, lang='japan', det_model_dir=det_model_dir, rect_model_dir=rect_model_dir, cls_model_dir=cls_model_dir)

    def detect(self, np_image):
        # np_image = np.asarray(image)
        paddle_boxes = self.ocr.ocr(np_image, cls=False, rec=False)
        boxes = [(int(box[0][0]), int(box[0][1]), int(box[2][0]), int(box[2][1])) for box in paddle_boxes]
        return boxes