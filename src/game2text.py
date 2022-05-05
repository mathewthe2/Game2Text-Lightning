
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from forwardscan import get_longest_match
from screenshot import get_screenshot
from screenshot.CaptureScreen import CaptureScreen
from tools import STR_Engine, OCR_Engine
from tools.str import STR
from tools.ocr import OCR
from util.cursor import cursor_position
from tooltip import Tooltip

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
        self.str_engine = STR_Engine.EAST
        self.ocr_engine = OCR_Engine.TESSERACT_DEFAULT

        self.str = STR(self.str_engine)
        self.ocr = OCR(self.ocr_engine)

        self.tooltip = None
        self.results = []
        self.characters = []

        # PYQT GUI
        
        # setting  the geometry of window
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

    def detect_character(self, point):
        if not self.results:
            return None
        total = []
        for characters in self.results:
            for character in characters:
                if character.touches_point(point):
                    total.append(character)
        return total

    def show_popup(self):
        x, y = cursor_position()
        touched_characters = self.detect_character((x, y))
        if touched_characters:
            glossary = touched_characters[0].text
            if self.tooltip is None:
                self.tooltip = Tooltip(glossary, x, y)
                self.tooltip.show()
            else:
                self.tooltip.setWindowTitle(glossary)
                self.tooltip.updateLabel(glossary)
                self.tooltip.move(x, y)
            
    
    def lightning(self):
        if (self.popup_timer.isActive()):
            self.popup_timer.stop()
            return
        screenshot = get_screenshot()

        # Scene Text Recognition
        cropped_images = self.str.get_cropped_images(screenshot)
        closest_image = self.str.get_closest_image(cropped_images, cursor_position())

        # OCR
        # self.results = [self.ocr.get_boxed_characters(cropped_image.get_image(), cropped_image.origin()) for cropped_image in cropped_images]
        boxed_characters = self.ocr.get_boxed_characters(closest_image.get_image(), closest_image.origin())
        self.results = [boxed_characters]

        self.popup_timer.start(40)

    def select_area(self):
        self.popup_timer.stop()
        self.hide()
        self.snippingWidget.start()
    
    def on_snipping_completed(self, data):
        self.show()
        self.setWindowState(QtCore.Qt.WindowState.WindowActive)
        image, origin, end = data
        point = (origin.x(), origin.y())
        boxed_characters = self.ocr.get_boxed_characters(image, point)
        self.results = [boxed_characters]
        self.popup_timer.start(40)
        
    def closeEvent(self, event):
        if self.tooltip:
            self.tooltip.close()

def main():
    App = QtWidgets.QApplication(sys.argv)
    window = Game2Text()
    window.show()

    sys.exit(App.exec())

if __name__ == '__main__':
    main()