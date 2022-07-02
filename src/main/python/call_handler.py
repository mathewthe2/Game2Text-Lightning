
from PyQt5.QtCore import QObject, pyqtSlot, QVariant
from japanese.pitch import Pitch
import json

# Bridge between PyQt and Web
class CallHandler(QObject):
    def __init__(self, appctxt, ankiconnect):
        super().__init__()
        self.appctxt = appctxt
        self.screenshot = None
        self.ankiconnect = ankiconnect
    
    def setScreenshot(self, screenshot):
        self.screenshot = screenshot

    @pyqtSlot(QVariant)
    def send_to_anki(self, args):
        vocab = json.loads(args)
        if self.screenshot is not None:
            vocab['screenshot'] = self.screenshot.base_64()
        result = self.ankiconnect.create_anki_note(vocab)
        print('created')
        print(result)

    @pyqtSlot(QVariant, result=str)
    def get_pitch(self, args):
        pitch_dictionary = Pitch(self.appctxt.get_resource('rikaisama/pitch_accents.sqlite'))
        pitch = pitch_dictionary.get_pitch(args[0], '' if len(args) <= 1 else args[1])
        print('pitch', pitch)
        return pitch
