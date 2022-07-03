import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from anki.anki_connect import AnkiConnect
from anki.anki_settings import AnkiSettings
from call_handler import CallHandler
from screenshot.hwnd_worker import HWNDWorker
from threading import Thread
from game2text.ocr import OCR
from config import Config
from control_panel import ControlPanel

class Main(QMainWindow):
    def __init__(self, appctxt):
        super().__init__()
        self.setGeometry(500, 500, 400, 400)
        self.setWindowTitle("Game2Text Lightning")
        self.hwnd_worker = HWNDWorker(interval=1000)
        self.anki_settings = AnkiSettings(appctxt)
        self.anki_connect = AnkiConnect(anki_settings=self.anki_settings)
        self.ocr = OCR(appctxt)
        self.call_handler = CallHandler(appctxt, self.anki_connect)
        self.config = Config(appctxt)
        self.control_panel = ControlPanel(self)
        self.setCentralWidget(self.control_panel)

        # Windows
        self.hwnd_worker.hwnd_signal.connect(self.on_receive_window_titles)
        self.hwnd_worker.start()

        # Anki
        self.load_anki()

    def on_receive_window_titles(self, windows):
        self.windows = windows
        self.control_panel.set_windows(self.windows)

    def fetch_models(self):
        self.models = self.anki_connect.fetch_anki_models()
        self.control_panel.set_models(self.models)

    def fetch_decks(self):
        self.decks =  self.anki_connect.fetch_anki_decks()
        self.control_panel.set_decks(self.decks)

    def capture(self):
        return self.control_panel.get_capture()
    
    def load_anki(self):
        model_thread = Thread(target = self.fetch_models)
        deck_thread = Thread(target = self.fetch_decks)
        model_thread.start()
        deck_thread.start()

def main():
    appctxt = ApplicationContext()       
    window = Main(appctxt)
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()