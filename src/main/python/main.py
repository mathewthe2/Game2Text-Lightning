import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QWidget
from screenshot.hwnd_manager import HWNDManager
from anki.anki_connect import AnkiConnect
from call_handler import CallHandler
from screenshot.capture_window import CaptureWindow
from screenshot.capture_screen import CaptureScreen
from screenshot import Capture_Mode
from threading import Thread
from ui.main_ui import UIMain
from game2text.ocr import OCR, OCR_Engine, paddle_models_path
from game2text import Game2Text

class Main(QMainWindow):
    def __init__(self, appctxt):
        super().__init__()
        self.setGeometry(500, 500, 400, 400)
        self.setWindowTitle("Game2Text Lightning")
        self.HWNDManager = HWNDManager()
        self.anki_connect = AnkiConnect(anki_models_path = appctxt.get_resource('anki/user_models.yaml'))
        self.ocr = OCR(appctxt.get_resource(paddle_models_path), OCR_Engine.PADDLE_OCR)
        self.call_handler = CallHandler(appctxt, self.anki_connect)
        self.control_panel = ControlPanel(self)
        self.setCentralWidget(self.control_panel)
        # Windows
        window_thread = Thread(target = self.fetch_windows)
        window_thread.start()

        # Anki
        model_thread = Thread(target = self.fetch_models)
        deck_thread = Thread(target = self.fetch_decks)
        model_thread.start()
        deck_thread.start()

    def fetch_models(self):
        self.models = self.anki_connect.fetch_anki_models()
        self.control_panel.set_models(self.models)

    def fetch_decks(self):
        self.decks =  self.anki_connect.fetch_anki_decks()
        self.control_panel.update_deck_options(self.decks)

    def fetch_windows(self):
        self.windows = self.HWNDManager.get_hwnd_titles()
        self.control_panel.set_windows(self.windows)

    def capture(self):
        return self.control_panel.get_capture()

class ControlPanel(QWidget, UIMain):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        # Window Capture
        self.windows = []
        self.capture_window = CaptureWindow()

        # Area Capture 
        self.snipping_widget = CaptureScreen()
        self.snipping_widget.onSnippingCompleted = self.on_snipping_completed
        self.snipped_capture = None

        self.call_handler = parent.call_handler # handle calls between web and python
        self.game2text = Game2Text(parent.ocr, parent.capture, self.call_handler)
        self.running_ocr = False
        self.capture_mode = Capture_Mode.WINDOW

        self.captureComboBox.currentIndexChanged.connect(self.select_capture_mode)
        self.captureWindowComboBox.currentIndexChanged.connect(self.select_window)
        self.modelComboBox.currentIndexChanged.connect(self.select_model)
        self.selectRegionButton.clicked.connect(self.select_area)
        self.start_button.clicked.connect(self.toggle_ocr)

        # Anki Settings
        self.anki_connect = parent.anki_connect
        self.models = []
        self.selected_model = None
        self.tableFields.on_change = self.on_anki_options_update


    def select_model(self, index):
        if self.models:
            self.selected_model = self.models[index]
            fields = self.selected_model.fields
            self.tableFields.setRowCount(len(fields))
            field_value_map = self.anki_connect.get_field_value_map(self.selected_model.model_name)
            self.tableFields.setData(fields, field_value_map)
            self.tableFields.show()
            # self.call_handler.set_model(self.selected_model.model_name)
            self.anki_connect.set_model(self.selected_model.model_name)

    def update_model_options(self, options):
        for option in options:
            self.modelComboBox.addItem(option)

    def update_deck_options(self, options):
        for option in options:
            self.deckComboBox.addItem(option)

    def set_models(self, models):
        self.models = models
        self.update_model_options([model.model_name for model in self.models])

    def set_windows(self, windows):
        self.windows = windows
        for window in windows:
             self.captureWindowComboBox.addItem(window)
        
    def select_capture_mode(self, index):
        self.capture_mode = Capture_Mode(index)

    def select_window(self, index):
        if self.windows:
            self.start_button.setEnabled(True)
            self.capture_window.setWindowTitle(self.windows[index])

    def get_capture(self):
        if self.capture_mode == Capture_Mode.WINDOW:
            return self.capture_window.get_capture()
        elif self.capture_mode == Capture_Mode.DESKTOP_AREA:
            return self.get_area_capture()
        else:
            return None

    def select_area(self):
        self.game2text.stop()
        self.snipping_widget.start()

    def get_area_capture(self):
        return self.snipping_widget.captureArea()

    def on_snipping_completed(self, capture_object):
        if capture_object.is_valid():
            self.snipped_capture = capture_object
            self.regionInfoLabel.setText(capture_object.get_region_info())
            self.start_button.setEnabled(True)

    def toggle_ocr(self):
        if self.game2text:
            if self.running_ocr:
                self.game2text.stop()
            else:
                self.game2text.run()
            self.running_ocr = not self.running_ocr

    def on_anki_options_update(self, user_field_map):
        self.anki_connect.update_user_model(self.selected_model.model_name, user_field_map)

def main():
    appctxt = ApplicationContext()       
    window = Main(appctxt)
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()