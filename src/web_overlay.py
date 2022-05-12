import sys, os
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from pathlib import Path

sys.argv.append("--disable-web-security")
bundle_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
rikaisama_path = 'file:///resources/rikaisama/'
web_path = 'file:///resources/web/'

class WebOverlay(QWebEngineView):
    ready = False
    containers = 0

    def __init__(self, x, y, w=800, h=300):
        super(WebOverlay, self).__init__()
        
        self.setGeometry(x, y, w, h)
        self.resize_fixed(w, h)
   
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.page().setBackgroundColor(Qt.transparent)
        self.load_html()

    def resize_fixed(self, w, h):
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.w = w                  
        self.h = h

    def setReady(self, ready):
        self.ready = ready 

    def load_html(self):
        raw_html = '<html><head><meta charset="utf-8" />'
        raw_html += '<link rel="stylesheet" href="{}">'.format(web_path + 'scale.css')
        raw_html += '<script src="{}"></script>'.format(web_path + 'scale.js')
        raw_html += '</head><body>'
        raw_html += '<div id="container-template" class="scale__container--js" style="hidden: true; position: absolute"></div>'
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'jedict.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'deinflect.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'data.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'config.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'options.js')
        raw_html += '<script src="{}"></script>'.format(rikaisama_path + 'raikaichan.js')
        raw_html += '</body></html>'
        self.setHtml(raw_html, baseUrl=QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))  
        self.loadFinished.connect(lambda x: self.setReady(True))

    def updateText(self, detection_box):
        if not self.ready:
            self.loadFinished.connect(lambda x: self.updateText(detection_box))
            return
        text_boxes = detection_box.text_boxes
        script = 'var templateContainer = document.getElementById("container-template");'
        # clear old textboxes
        for existing_index in range(self.containers):
                script += 'document.body.removeChild(document.getElementById("container-{}"));'.format(existing_index)
        # add new textboxes
        for index, text_box in enumerate(text_boxes):
            text = text_box.text
            x, y, x2, y2 = text_box.box
            w = text_box.width()
            h = text_box.height()
            script += 'var containerClone = templateContainer.cloneNode(templateContainer);'
            script += 'containerClone.id = "container-{}";'.format(index)
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
        self.page().runJavaScript(script)
        self.containers = len(text_boxes)    