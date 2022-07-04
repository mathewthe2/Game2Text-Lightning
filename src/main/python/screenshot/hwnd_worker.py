from PyQt5.QtCore import QThread, QTimer, pyqtSignal, QEventLoop
from .hwnd_manager import HWNDManager

class HWNDWorker(QThread):
    window_signal = pyqtSignal(list)
    def __init__(self, interval):
        super(QThread, self).__init__()
        self.hwnd_manager = HWNDManager()
        self.interval = interval
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.emit_windows)

    def run(self):
        self.timer.start(self.interval)
        loop = QEventLoop()
        loop.exec_()

    def emit_windows(self):
        windows = self.hwnd_manager.get_window_objects()
        self.window_signal.emit(windows)
    