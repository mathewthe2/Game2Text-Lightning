
from PyQt5 import QtCore
from util.box import box_to_qt
from util.cursor import cursor_position
from util.detection_box import grouped_boxes
from web_overlay import WebOverlay
from pyqt_custom.blur_window import BlurWindow

POPUP_INTERVAL = 45
RECAPTURE_INTERVAL = 500

class Game2Text():
    def __init__(self, ocr, capture):
        self.ocr = ocr
        self.capture = capture
        self.is_processing_image = False
        self.active_capture_object = None
        self.is_processing_image = False
        self.status = ''

        self.overlay_window = WebOverlay()
        self.blur_window = None
        self.detection_boxes = []
        self.text_boxes = []
        self.results = []
        self.characters = []

        self.popup_timer = QtCore.QTimer()
        self.popup_timer.timeout.connect(self.show_popup)
        
        self.recapture_timer = QtCore.QTimer()
        self.recapture_timer.timeout.connect(self.recapture)

    def run(self):
        capture_object = self.capture()
        if not capture_object:
            return
        image_object = capture_object.image_object
        origin = capture_object.get_origin_point()
        end = capture_object.get_end_point()
        
        self.is_processing_image = True
        # image_object = ImageObject(image, IMAGE_TYPE.CV)
        self.setActiveImage(capture_object)
        self.text_boxes = self.ocr.get_text(image_object)
        self.detection_boxes = grouped_boxes(self.text_boxes, origin=(origin.x(), origin.y()))
        self.is_processing_image = False
        self.overlay_window = WebOverlay(origin.x(), origin.y(), abs(end.x()-origin.x()), abs(end.y()-origin.y()))
        self.overlay_window.setScreenshot(image_object)
        self.popup_timer.start(POPUP_INTERVAL)
        self.recapture_timer.start(RECAPTURE_INTERVAL)

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
            new_capture = self.capture()
            origin = new_capture.get_origin_point()
            end = new_capture.get_end_point()
            is_new_image = not self.active_capture_object.is_similar(new_capture)
            if not is_new_image:
                return
            self.is_processing_image = True
            self.status = 'recapturing...'
            print(self.status)

            self.overlay_window.setGeometry(origin.x(), origin.y(), abs(end.x()-origin.x()), abs(end.y()-origin.y()))
            self.overlay_window.setScreenshot(new_capture)

            text_boxes = self.ocr.get_text(new_capture)
            self.status = 'got text...'
            print(self.status)
            # stop if same textboxes and same origin
            # same_text_boxes = len(text_boxes) == len(self.text_boxes)
            # if same_text_boxes:
            #     for i in range(0, len(text_boxes)):
            #         if text_boxes[i].box != self.text_boxes[i].box or text_boxes[i].text != self.text_boxes[i].text:
            #             same_text_boxes = False
            # if same_text_boxes:
            #     self.is_processing_image = False
            #     return
            self.detection_boxes = grouped_boxes(text_boxes, origin=(origin.x(), origin.y()))
            
            self.active_capture_object = new_capture
            self.is_processing_image = False

    def setActiveImage(self, capture_object):
        self.active_capture_object = capture_object

    def stop(self):
        self.popup_timer.stop()
        self.recapture_timer.stop()
        if self.overlay_window:
            self.overlay_window.close()
        if self.blur_window:
            self.blur_window.close()