from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys, os
from web_overlay import WebOverlay
from PyQt5.QtCore import QObject, pyqtSlot, QVariant
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

class WebOverlayTest():
    def __init__(self):
        self.call_handler = CallHandler()
        self.web_overlay = WebOverlay(0, 0, 550, 300, self.call_handler)
        self.web_overlay.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.web_overlay.setAttribute(Qt.WA_NoSystemBackground, False)
        self.web_overlay.setAttribute(Qt.WA_TranslucentBackground, False)

    def run(self):
        self.web_overlay.loadFinished.connect(lambda x: self.testText('出荷を担当するから'))
        self.web_overlay.show()

    def testText(self, text, x=0, y=0, w=300, h=50):
        script = 'var templateContainer = document.getElementById("container-template");'
        script += 'var containerClone = templateContainer.cloneNode(templateContainer);'
        script += 'containerClone.id = "container-1";'
        script += 'containerClone.style.width = "{}px";'.format(w)
        script += 'containerClone.style.height = "{}px";'.format(h)
        script += 'containerClone.style.top = "{}px";'.format(y)
        script += 'containerClone.style.left = "{}px";'.format(x)
        script += 'var textElement = document.createElement("div");textElement.className = "scale--js";'
        script += 'textElement.innerHTML = "{}";'.format(text)
        script += 'containerClone.appendChild(textElement);'
        script += 'containerClone.hidden = false;'
        script += 'document.body.appendChild(containerClone);'
        script += 'myScaleFunction();'
        self.web_overlay.page().runJavaScript(script)

import pyperclip

class CallHandler(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(QVariant)
    def send_to_anki(self, args):
        vocab = json.loads(args)
        print(vocab)
    @pyqtSlot(QVariant, result=str)
    def get_pitch(self, args):
        return ''
    @pyqtSlot(QVariant)
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = WebOverlayTest()
    test.run()
    sys.exit(app.exec())