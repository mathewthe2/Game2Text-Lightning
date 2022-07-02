from PyQt5.QtCore import QThread, pyqtSignal

class CaptureWorker(QThread):
    capture_signal = pyqtSignal(object)
    def __init__(self, capture):
        super(QThread, self).__init__()
        self.capture = capture

    def run(self):
        capture_object = self.capture()
        self.capture_signal.emit(capture_object)
