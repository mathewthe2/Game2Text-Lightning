import sys, os
import json
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, Qt
from call_handler import CallHandler

sys.argv.append("--disable-web-security")

RIKAISAMA_JS_LIST = ['radicals.js', 'kanji.js', 'jedict.js', 'deinflect.js', 'data.js', 'config.js', 'options.js', 'raikaichan.js']
FONT_REGULAR = 'web/fonts/M_PLUS_1p/MPLUS1p-Regular.ttf'
FONT_BOLD = 'web/fonts/M_PLUS_1p/MPLUS1p-Medium.ttf'

appctxt = ApplicationContext()

def getResourceUrl(filename):
    return QUrl.fromLocalFile(appctxt.get_resource(filename)).toString()

class WebOverlay(QWebEngineView):
    ready = False
    containers = 0

    def __init__(self, x=0, y=0, w=800, h=300):
        super(WebOverlay, self).__init__()    

        # Web channel
        self.channel = QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject('handler', self.handler)
        self.page().setWebChannel(self.channel)

        # Window Attributes
        self.setGeometry(x, y, w, h)
        self.resize_fixed(w, h)
   
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
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
        print('ready!')

    def load_html(self):
        raw_html = '<html><head><meta charset="utf-8" />'
        raw_html += '<script src="qrc:///qtwebchannel/qwebchannel.js"></script>'
        raw_html += '''
        <style>
            @font-face {{
                font-family: M_PLUS_1p;
                src: url('{}');
            }}
            @font-face {{
                font-family: M_PLUS_1p;
                src: url('{}');
                font-weight: bold;
            }}
            div {{
                font-family: M_PLUS_1p;
            }}
        </style>
        '''.format(getResourceUrl(FONT_REGULAR), getResourceUrl(FONT_BOLD))
        raw_html += '<link rel="stylesheet" href="{}">'.format(getResourceUrl("web/scale.css"))
        raw_html += '<link rel="stylesheet" href="{}">'.format(getResourceUrl("rikaisama/popup-blue.css"))
        raw_html += '<script src="{}"></script>'.format(getResourceUrl("web/scale.js"))
        raw_html += '</head><body>'
        raw_html += '<div id="container-template" class="scale__container--js" style="hidden: true; position: absolute"></div>'
        for js_file in RIKAISAMA_JS_LIST:
            raw_html += '<script src="{}"></script>'.format(getResourceUrl('rikaisama/' + js_file))
        raw_html += '''
        <script language="JavaScript">
         new QWebChannel(qt.webChannelTransport, function (channel) {
          window.handler = channel.objects.handler;
         // handler.send_to_anki(JSON.stringify({"a": 3}));
        });
        </script>
        '''
        raw_html += '</body></html>'
        self.setHtml(raw_html, baseUrl=QUrl.fromLocalFile(appctxt.get_resource("web")))
        self.loadFinished.connect(lambda x: self.setReady(True))

    def setScreenshot(self, screenshot):
        self.handler.setScreenshot(screenshot)

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
            postText = '' if (index >= len(text_boxes)-1) else '<br/><span hidden>' + ''.join([textbox.text for textbox in text_boxes[index+1:]]) + '</span>'
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
            script += 'textElement.innerHTML = "{}";'.format(text+postText)
            script += 'containerClone.appendChild(textElement);'
            script += 'containerClone.hidden = false;'
            script += 'document.body.appendChild(containerClone);'
            script += 'myScaleFunction();'
        self.page().runJavaScript(script)
        self.containers = len(text_boxes)    