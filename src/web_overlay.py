from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pathlib import Path
import os, sys

from util.box import box_to_qt

sys.argv.append("--disable-web-security")
bundle_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
rikaisama_path = 'file:///resources/rikaisama/'
web_path = 'file:///resources/web/'

class WebOverlay(QtWidgets.QWidget):
    dirty = True
    def __init__(self, x, y, w=800, h=300):
        super(WebOverlay, self).__init__()

        self.setGeometry(x, y, w, h)
        self.resize_fixed(w, h)

        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint | Qt.FramelessWindowHint
        )
        
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        # limit widget AND layout margins
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.browser = QWebEngineView()
        # self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.browser.page().setBackgroundColor(Qt.transparent)
        layout.addWidget(self.browser)

        # create a "placeholder" widget for the screen grab geometry
        self.grabWidget = QtWidgets.QWidget()
        self.grabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.grabWidget)


    def resize_fixed(self, w, h):
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.w = w                  
        self.h = h

    def updateText(self, detection_box):
        text_boxes = detection_box.text_boxes
        # grouped_box = detection_box.box
        
        # Update Text
        raw_html = '<html><head><meta charset="utf-8" />'
        raw_html += '<link rel="stylesheet" href="{}">'.format(web_path + 'scale.css')
        raw_html += '<script src="{}"></script>'.format(web_path + 'scale.js')
        raw_html += '</head><body>'
        for text_box in text_boxes:
            text = text_box.text
            x, y, x2, y2 = text_box.box
            w = text_box.width()
            h = text_box.height()
            raw_html += '<div class="scale__container--js" style="width:' + str(w) + 'px; height:' + str(h) + 'px; position:absolute; top: ' + str(y) + 'px; left: ' + str(x) + 'px;">'
            raw_html += '<div class="scale--js">' + text + '</div>'
            raw_html += '</div>'
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'jedict.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'deinflect.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'data.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'config.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'options.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'raikaichan.js')
        raw_html += '</body></html>'
        self.browser.setHtml(raw_html, baseUrl=QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))  

    # https://stackoverflow.com/a/57742146
    def updateMask(self):
        # get the *whole* window geometry, including its titlebar and borders
        frameRect = self.frameGeometry()

        # get the grabWidget geometry and remap it to global coordinates
        grabGeometry = self.grabWidget.geometry()
        grabGeometry.moveTopLeft(self.grabWidget.mapToGlobal(QtCore.QPoint(0, 0)))

        # get the actual margins between the grabWidget and the window margins
        left = frameRect.left() - grabGeometry.left()
        top = frameRect.top() - grabGeometry.top()
        right = frameRect.right() - grabGeometry.right()
        bottom = frameRect.bottom() - grabGeometry.bottom()

        # reset the geometries to get "0-point" rectangles for the mask
        frameRect.moveTopLeft(QtCore.QPoint(0, 0))
        grabGeometry.moveTopLeft(QtCore.QPoint(0, 0))

        # create the base mask region, adjusted to the margins between the
        # grabWidget and the window as computed above
        region = QtGui.QRegion(frameRect.adjusted(left, top, right, bottom))
        # "subtract" the grabWidget rectangle to get a mask that only contains
        # the window titlebar, margins and panel
        region -= QtGui.QRegion(grabGeometry)
        self.setMask(region)

        # update the grab size according to grabWidget geometry
        # self.widthLabel.setText(str(self.grabWidget.width()))
        # self.heightLabel.setText(str(self.grabWidget.height()))

    def resizeEvent(self, event):
        super(WebOverlay, self).resizeEvent(event)
        # the first resizeEvent is called *before* any first-time showEvent and
        # paintEvent, there's no need to update the mask until then; see below
        if not self.dirty:
            self.updateMask()

    def paintEvent(self, event):
        super(WebOverlay, self).paintEvent(event)
        # on Linux the frameGeometry is actually updated "sometime" after show()
        # is called; on Windows and MacOS it *should* happen as soon as the first
        # non-spontaneous showEvent is called (programmatically called: showEvent
        # is also called whenever a window is restored after it has been
        # minimized); we can assume that all that has already happened as soon as
        # the first paintEvent is called; before then the window is flagged as
        # "dirty", meaning that there's no need to update its mask yet.
        # Once paintEvent has been called the first time, the geometries should
        # have been already updated, we can mark the geometries "clean" and then
        # actually apply the mask.
        if self.dirty:
            self.updateMask()
            self.dirty = False

# if __name__ == '__main__':
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     w = WebOverlay(500, 500, 500, 500)
#     w.show()
#     # w.testText('家のお使いだったから')
#     w.blur_window = BlurWindow(500, 500, 100, 100)
#     w.blur_window.show()
#     sys.exit(app.exec_())