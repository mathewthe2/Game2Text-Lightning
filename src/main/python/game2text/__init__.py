from PyQt5 import QtCore
from util.box import box_to_qt
from util.cursor import cursor_position
from util.detection_box import grouped_boxes
from pyqt_custom.blur_window import BlurWindow
from .web_overlay import WebOverlay
from .workers.ocr_worker import OcrWorker
from .workers.capture_worker import CaptureWorker

POPUP_INTERVAL = 100
RECAPTURE_INTERVAL = 500

class Game2Text():
    def __init__(self, ocr, capture, handler):
        super().__init__()
        self.ocr = ocr
        self.capture = capture
        self.handler = handler
        self.is_processing_image = False
        self.active_capture_object = None
        self.is_processing_image = False
        self.status = ''

        self.overlay_window = None
        self.blur_window = None
        self.detection_boxes = []
        self.text_boxes = []
        self.results = []
        self.characters = []

        self.popup_timer = QtCore.QTimer()
        self.popup_timer.timeout.connect(self.show_popup)
        
        self.recapture_timer = QtCore.QTimer()
        self.recapture_timer.timeout.connect(self.recapture)

        self.ocr_worker = OcrWorker(self.ocr)
        self.ocr_worker.text_boxes_signal.connect(self.on_receive_text_boxes)

        self.capture_worker = CaptureWorker(self.capture)
        self.capture_worker.capture_signal.connect(self.on_receive_capture)

    def run(self):
        self.capture_worker.start()
        self.popup_timer.start(POPUP_INTERVAL)
        self.recapture_timer.start(RECAPTURE_INTERVAL)

    def process_ocr(self, capture_object, text_boxes):
        self.text_boxes = text_boxes
        image_object = capture_object.image_object
        origin = capture_object.get_origin_point()
        end = capture_object.get_end_point()
        self.detection_boxes = grouped_boxes(self.text_boxes, origin=(origin.x(), origin.y()))
        self.is_processing_image = False
        window_geometry = (origin.x(), origin.y(), abs(end.x()-origin.x()), abs(end.y()-origin.y()))
        if not self.overlay_window:
            self.overlay_window = WebOverlay(*window_geometry, self.handler)
        else:
            self.overlay_window.setGeometry(*window_geometry)
        self.overlay_window.setScreenshot(image_object)

    def detect_touched_box(self, point):
        if not self.detection_boxes:
            return None
        total = [detection_box for detection_box in self.detection_boxes if detection_box.touches_point(point)]
        return total

    def show_popup(self):
        x, y = cursor_position()
        touched_boxes = self.detect_touched_box((x, y))
        if touched_boxes:
            if self.overlay_window.isVisible():
                return

            # Assuming that all touched boxes are merged together into the first box
            touched_box = touched_boxes[0]
            self.overlay_window.updateText(touched_box)
            blur_x, blur_y, blur_w, blur_h = box_to_qt(touched_box.padded_box(30))
            self.blur_window = BlurWindow(blur_x, blur_y, blur_w, blur_h)
            self.blur_window.show()

            if not self.overlay_window.isVisible():
                self.overlay_window.show()
        else:
            if self.overlay_window and not self.is_processing_image:
                self.overlay_window.hide()
            if self.blur_window and not self.is_processing_image:
                self.blur_window.hide()

    def recapture(self):
        overlay_window_visible = False
        if self.overlay_window:
            overlay_window_visible = self.overlay_window.isVisible()
        if self.active_capture_object and not self.is_processing_image and not overlay_window_visible:
            # capture new image
            self.capture_worker.start()

    def on_receive_capture(self, capture_object):
        if not capture_object:
            return
        self.is_processing_image = True
        if self.active_capture_object:
            is_new_image = not self.active_capture_object.is_similar(capture_object)
            if not is_new_image:
                self.is_processing_image = False
                return
        self.setActiveImage(capture_object)
        self.ocr_worker.set_capture(capture_object)
        self.ocr_worker.start()

    def on_receive_text_boxes(self, result):
        text_boxes, capture = result
        self.process_ocr(capture, text_boxes)

    def setActiveImage(self, capture_object):
        self.active_capture_object = capture_object

    def stop(self):
        self.popup_timer.stop()
        self.recapture_timer.stop()
        if self.overlay_window:
            self.overlay_window.close()
        if self.blur_window:
            self.blur_window.close()