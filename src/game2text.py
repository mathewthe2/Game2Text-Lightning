
import sys, time
from PyQt5 import QtWidgets, QtCore, QtGui
from numpy import False_
# from forwardscan import get_longest_match
from screenshot import get_screenshot_image
from screenshot.CaptureScreen import CaptureScreen
from g2t_tools import STR_Engine, OCR_Engine
from g2t_tools.str import STR
from g2t_tools.ocr import OCR
from util.cursor import cursor_position
from util.image_object import IMAGE_TYPE, ImageObject
from image_box import ImageBox
from overlay_window import OverlayWindow

# Optical Character Recognition Engine
# class Capture_Mode(Enum):
#     LIGHTNING = 1
#     AUTO = 2
#     MANUAL = 3

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200

class Game2Text(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.str_engine = STR_Engine.PADDLE
        self.ocr_engine = OCR_Engine.TESSERACT

        self.str = STR(self.str_engine)
        self.ocr = OCR(self.ocr_engine)

        self.active_image_box = None
        self.is_processing_image = False

        self.overlay_window = None
        self.image_boxes = []
        self.results = []
        self.characters = []

        # PYQT GUI
        
        # setting the geometry of window
        self.setGeometry(500, 500, WINDOW_WIDTH, WINDOW_HEIGHT)

        # set the title
        self.setWindowTitle("Game2Text")

        # set always on top
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        pybutton = QtWidgets.QPushButton('OCR', self)
        pybutton.resize(100,32)
        pybutton.move(50, 50)    
        pybutton.clicked.connect(self.lightning)

        sekectButton = QtWidgets.QPushButton('Select', self)
        sekectButton.resize(100,32)
        sekectButton.move(50, 100)    
        sekectButton.clicked.connect(self.select_area) 

        self.snippingWidget = CaptureScreen()
        self.snippingWidget.onSnippingCompleted = self.on_snipping_completed

        self.popup_timer = QtCore.QTimer()
        self.popup_timer.timeout.connect(self.show_popup)
        
        self.recapture_timer = QtCore.QTimer()
        self.recapture_timer.timeout.connect(self.recapture)

    def detect_image_box(self, point):
        if not self.image_boxes:
            return None
        total = [image_box for image_box in self.image_boxes if image_box.touches_point(point)]
        return total

    def show_popup(self):
        x, y = cursor_position()
        # print(x, y)
        touched_image_boxes = self.detect_image_box((x, y))
        if touched_image_boxes:
            glossary = touched_image_boxes[0].text
            box_x1, box_y1, box_w, box_h = touched_image_boxes[0].rect()
            if self.overlay_window is None:
                self.overlay_window = OverlayWindow(glossary, box_x1, box_y1, box_w, box_h)
            else:
                self.overlay_window.setWindowTitle(glossary)
                self.overlay_window.updateText(glossary)
                self.overlay_window.resize_fixed(box_w, box_h)
                self.overlay_window.move(box_x1, box_y1)
            if not self.overlay_window.isVisible():
                self.overlay_window.show()
        else:
            if self.overlay_window and not self.is_processing_image:
                self.overlay_window.hide()
            
    def lightning(self):
        if (self.popup_timer.isActive()):
            self.popup_timer.stop()
            return

        screenshot = get_screenshot_image()

        # Scene Text Recognition
        image_object = ImageObject(screenshot, IMAGE_TYPE.PIL)
        image_boxes = self.str.get_cropped_image_boxes(image_object)

        closest_image = self.str.get_closest_image(image_boxes, cursor_position())

        # OCR
        closest_image.set_text(self.ocr.get_text(closest_image.image))
        print(closest_image.text)
        print(closest_image.box)
        self.image_boxes = [closest_image]

        self.popup_timer.start(40)

    def select_area(self):
        self.popup_timer.stop()
        self.recapture_timer.stop()
        self.hide()
        self.snippingWidget.start()

    def setActiveImage(self, image, origin, end):
        box = origin.x(), origin.y(), end.x(), end.y()
        self.active_image_box = ImageBox(box, image)
    
    def on_snipping_completed(self, data):
        self.show()
        self.setWindowState(QtCore.Qt.WindowState.WindowActive)
        self.is_processing_image = True
        image, origin, end = data
        image_object = ImageObject(image, IMAGE_TYPE.CV)
        self.setActiveImage(image_object.get_image(IMAGE_TYPE.PIL), origin, end)
        image_boxes = self.str.get_cropped_image_boxes(image_object)
        for image_box in image_boxes:
            image_box.set_text(self.ocr.get_text(image_box.image))
            image_box.adjust_to_origin((origin.x(), origin.y()))
            print(image_box.text)
        self.image_boxes = image_boxes
        self.is_processing_image = False
        self.popup_timer.start(40)
        self.recapture_timer.start(1000)

    def recapture(self):
        overlay_window_visible = False
        if self.overlay_window:
            overlay_window_visible = self.overlay_window.isVisible()
        if self.active_image_box and not self.is_processing_image and not overlay_window_visible:
            # capture new image
            screenshot = get_screenshot_image()
            new_capture = screenshot.crop(self.active_image_box.box)
            new_capture_box = ImageBox(self.active_image_box.box, new_capture)
            is_new_image = not self.active_image_box.is_similar(new_capture_box)
            if not is_new_image:
                return
            self.is_processing_image = True
            origin_x, origin_y, end_x, end_y = self.active_image_box.box
            image_object = ImageObject(new_capture, IMAGE_TYPE.PIL)
            image_boxes = self.str.get_cropped_image_boxes(image_object)
            if len(image_boxes) <= 0:
                self.is_processing_image = False
                return
            same_image_boxes = len(image_boxes) == len(self.image_boxes)
            if same_image_boxes:
                for i in range(0, len(image_boxes)):
                    image_boxes[i].adjust_to_origin((origin_x, origin_y))
                    if image_boxes[i].box != self.image_boxes[i].box:
                        same_image_boxes = False
            if same_image_boxes:
                self.is_processing_image = False
                return
            for image_box in image_boxes:
                image_box.set_text(self.ocr.get_text(image_box.image))
                print(image_box.text)
            self.image_boxes = image_boxes
            self.active_image_box = new_capture_box
            self.is_processing_image = False

    def closeEvent(self, event):
        if self.overlay_window:
            self.overlay_window.close()

def main():
    App = QtWidgets.QApplication(sys.argv)
    window = Game2Text()
    window.show()

    sys.exit(App.exec())

if __name__ == '__main__':
    main()