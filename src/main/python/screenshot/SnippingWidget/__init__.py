from .WinSnipper import WinSnipper
from .MacSnipper import MacSnipper
import sys

class SnippingWidget():
    def __init__(self, onSnippingCompleted=None):
        if sys.platform == 'darwin':
            self.snipper = MacSnipper()
        else:
            self.snipper = WinSnipper()
        if onSnippingCompleted is not None:
            self.snipper.onSnippingCompleted = onSnippingCompleted

    def start(self):
        self.snipper.start()

    def captureArea(self):
        return self.snipper.captureArea()