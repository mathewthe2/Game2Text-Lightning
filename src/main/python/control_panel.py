import logging
from PyQt5.QtWidgets import QWidget
from screenshot.capture_window import CaptureWindow
from screenshot.capture_screen import CaptureScreen
from screenshot import Capture_Mode
from ui.main_ui import UIMain
from game2text import Game2Text

class ControlPanel(QWidget, UIMain):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        # Window Capture
        self.windows = []
        self.selected_window = None
        self.capture_window = CaptureWindow()

        # Area Capture 
        self.snipping_widget = CaptureScreen()
        self.snipping_widget.onSnippingCompleted = self.on_snipping_completed
        self.snipped_capture = None

        self.game2text = Game2Text(parent.ocr, parent.capture, parent.call_handler)
        self.running_ocr = False
        self.capture_mode = Capture_Mode.WINDOW

        self.captureComboBox.currentIndexChanged.connect(self.select_capture_mode)
        self.captureWindowComboBox.activated.connect(self.select_window)
        self.deckComboBox.currentIndexChanged.connect(self.on_deck_change)
        self.deckComboBox.activated.connect(self.select_deck)
        self.modelComboBox.currentIndexChanged.connect(self.on_model_change)
        self.modelComboBox.activated.connect(self.select_model)
        self.selectRegionButton.clicked.connect(self.select_area)
        self.start_button.clicked.connect(self.toggle_ocr)
        self.reloadAnkiButton.clicked.connect(parent.load_anki)

        self.resizeWidthInput.textChanged.connect(self.set_resize_width)
        self.resizeHeightInput.textChanged.connect(self.set_resize_height)
        self.resizeCheckBox.stateChanged.connect(self.toggle_resize)

        # Anki Settings
        self.anki_connect = parent.anki_connect
        self.anki_settings = parent.anki_settings
        self.config = parent.config
        self.decks = []
        self.models = []
        self.deck_combo_ready = False
        self.model_combo_ready = False
        self.selected_model = None
        self.tableFields.on_change = self.on_anki_options_update

    def on_deck_change(self, index):
        if not self.deck_combo_ready:
            deck, model = self.anki_settings.get_default_deck_model()
            if deck and deck in self.decks:
                index = self.decks.index(deck)
                self.deckComboBox.setCurrentIndex(index)
                self.select_deck(index, persist=False)
            else:
                self.deckComboBox.setCurrentIndex(-1)
            self.deck_combo_ready = True

    def select_deck(self, index, persist=True):
        if self.decks:
            deck = self.decks[index]
            self.anki_connect.set_deck(deck)
            if persist:
                self.anki_settings.update_default_deck(deck)

    def on_model_change(self, index):
        if not self.model_combo_ready:
            deck, model = self.anki_settings.get_default_deck_model()
            model_names = [model.model_name for model in self.models]
            if model and model in model_names:
                index = model_names.index(model)
                self.modelComboBox.setCurrentIndex(index)
                self.select_model(index, persist=False)
            else:
                self.modelComboBox.setCurrentIndex(-1)
            self.model_combo_ready = True

    def select_model(self, index, persist=True):
        if self.models:
            self.selected_model = self.models[index]
            fields = self.selected_model.fields
            self.tableFields.setRowCount(len(fields))
            field_value_map = self.anki_settings.get_field_value_map(self.selected_model.model_name)
            self.tableFields.setData(fields, field_value_map)
            self.tableFields.show()
            self.anki_connect.set_model(self.selected_model.model_name)
            if persist:
                self.anki_settings.update_default_model(self.selected_model.model_name)

    def set_decks(self, decks):
        self.decks = decks
        self.deckComboBox.addItems(decks)

    def set_models(self, models):
        self.models = models
        self.modelComboBox.addItems([model.model_name for model in self.models])

    def set_windows(self, windows):
        self.windows = windows
        self.captureWindowComboBox.clear()
        new_selected_index = -1
        for index, window in enumerate(windows):
            self.captureWindowComboBox.addItem(window)
            if window == self.selected_window:
                new_selected_index = index
        self.captureWindowComboBox.setCurrentIndex(new_selected_index)

    def select_capture_mode(self, index):
        self.capture_mode = Capture_Mode(index)

    def select_window(self, index):
        if self.windows:
            self.start_button.setEnabled(True)
            self.selected_window = self.windows[index]
            self.capture_window.setWindowTitle(self.selected_window)

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
        self.anki_settings.update_user_model(self.selected_model.model_name, user_field_map)

    def toggle_resize(self, int):
        if self.resizeCheckBox.isChecked():
            self.config.write('IMAGECONFIG', {'resize_screenshot': 'true'})
        else:
            self.config.write('IMAGECONFIG', {'resize_screenshot': 'false'})

    def set_resize_width(self, text):
        try:
            width = int(text)
        except:
            logging.error("width not a number")
        finally:
            if width and width > 0:
                self.config.write('IMAGECONFIG', {'resize_screenshot_max_width': text})

    def set_resize_height(self, text):
        try:
            height = int(text)
        except:
            logging.error("width not a number")
        finally:
            if height and height > 0:
                self.config.write('IMAGECONFIG', {'resize_screenshot_max_height': text})
