from PyQt5.QtCore import QSettings

class SettingsController():
    def __init__(self):
        self.settings = QSettings("Game2Text", "App")

    def set_value(self, key, value):
        self.settings.setValue(key, value)

    def get_value(self, key):
        return self.settings.value(key)