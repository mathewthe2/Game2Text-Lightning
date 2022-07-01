from paddleocr import PaddleOCR
from pathlib import Path
from text_box import TextBox

class Paddle_OCR():
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

    def extract_text(self, np_image):
        result = self.ocr.ocr(np_image, cls=False)
        paddle_boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        print('result', txts)
        # scores = [line[1][1] for line in result]
        boxes = [(int(box[0][0]), int(box[0][1]), int(box[2][0]), int(box[2][1])) for box in paddle_boxes]
        text_boxes = [TextBox(txts[index], box) for index, box in enumerate(boxes)]
        return text_boxes