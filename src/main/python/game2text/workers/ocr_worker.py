from PyQt5.QtCore import QThread, pyqtSignal

class OcrWorker(QThread):
    text_boxes_signal = pyqtSignal(tuple)
    def __init__(self, ocr):
        super(QThread, self).__init__()
        self.ocr = ocr
        self.capture = None
    
    def set_capture(self, capture):
        self.capture = capture

    def run(self):
        if self.capture:
            text_boxes = self.ocr.get_text(self.capture.image_object)
            self.text_boxes_signal.emit((text_boxes, self.capture))
