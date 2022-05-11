import sys, os
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QDir, QUrl, Qt
from PyQt5.QtGui import QPainter, QPen, QPalette
from BlurWindow.blurWindow import blur
from pathlib import Path

from matplotlib.pyplot import text

sys.argv.append("--disable-web-security")
bundle_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
rikaisama_path = Path(bundle_dir, 'resources', 'rikaisama')
rikaisama_path = 'file:///resources/rikaisama/'
web_path = 'file:///resources/web/'

class WebOverlay(QWebEngineView):
    def __init__(self, text, x, y, w=800, h=300):
        super(WebOverlay, self).__init__()
        
        self.setGeometry(x, y, w, h)
        self.resize_fixed(w, h)
        # self.updateText()
   
        # self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.page().setBackgroundColor(Qt.transparent)

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.7)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))   
        painter.drawRect(self.rect())

    def resize_fixed(self, w, h):
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.w = w                  
        self.h = h
 
    # pass detection box and show all 
    def updateText(self, text_boxes):
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
        self.setHtml(raw_html, baseUrl=QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))  

    # def updateText(self, text, x=0, y=0, w=50, h=50):
    #     raw_html = '<html><head><meta charset="utf-8" />'
    #     raw_html += '<link rel="stylesheet" href="{}">'.format(web_path + 'scale.css')
    #     raw_html += '<script src="{}"></script>'.format(web_path + 'scale.js')
    #     raw_html += '</head><body>'
    #     raw_html += '<div class="scale__container--js" style="width:' + str(w) + 'px; height:' + str(h) + 'px; position:absolute; top: ' + str(y) + 'px; left: ' + str(x) + 'px;">'
    #     raw_html += '<div class="scale--js">' + text + '</div>'
    #     raw_html += '</div>'
    #     raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'jedict.js')
    #     raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'deinflect.js')
    #     raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'data.js')
    #     raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'config.js')
    #     raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'options.js')
    #     raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'raikaichan.js')
    #     raw_html += '</body></html>'
    #     self.setHtml(raw_html, baseUrl=QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))  
        

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mw = WebOverlay('家のお使いだったから', 500, 500, 550, 300)
#     mw.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
#     mw.show()
#     sys.exit(app.exec())