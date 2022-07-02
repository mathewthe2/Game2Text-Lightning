from PyQt5.QtWidgets import QMessageBox

class Message():
    def __init__():
        pass
    
    def show_error(self, error_text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_text)
        msg.setInformativeText('More information')
        msg.setWindowTitle("Error")
        msg.exec_()