from PyQt5 import QtWidgets, QtCore, QtGui
# import cv2
# import numpy as np

class CaptureScreen(QtWidgets.QSplashScreen):
    """QSplashScreen, that track mouse event for capturing screenshot."""
    def __init__(self):
        """"""
        super(CaptureScreen, self).__init__()
 
        # Points on screen marking the origin and end of regtangle area.
        self.origin = QtCore.QPoint(0,0)
        self.end = QtCore.QPoint(0,0)
 
        # A drawing widget for representing bounding area
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
 
        self.createDimScreenEffect()
 
    def createDimScreenEffect(self):
        """Fill splashScreen with black color and reduce the widget opacity to create dim screen effect"""
 
        # Get the screen geometry of the main desktop screen for size ref
        primScreenGeo = QtGui.QGuiApplication.primaryScreen().geometry()
 
        screenPixMap = QtGui.QPixmap(primScreenGeo.width(), primScreenGeo.height())
        screenPixMap.fill(QtGui.QColor(0,0,0))
 
        self.setPixmap(screenPixMap)
 
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setWindowOpacity(0.4)
 
    def mousePressEvent(self, event):
        """Show rectangle at mouse position when left-clicked"""
        if event.button() == QtCore.Qt.LeftButton:
            self.origin = event.pos()
 
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
            self.rubberBand.show()
 
    def mouseMoveEvent(self, event):
        """Resize rectangle as we move mouse, after left-clicked."""
        self.rubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
 
    def mouseReleaseEvent(self, event):
        """Upon mouse released, ask the main desktop's QScreen to capture screen on defined area."""
        if event.button() == QtCore.Qt.LeftButton:
            self.end = event.pos()
 
            self.rubberBand.hide()
            # self.hide()
            self.close()
 
            primaryScreen = QtGui.QGuiApplication.primaryScreen()
            grabbedPixMap = primaryScreen.grabWindow(0, self.origin.x(), self.origin.y(), self.end.x()-self.origin.x(), self.end.y()-self.origin.y())
            # self.Pixmap_to_Opencv(grabbedPixMap)
            # grabbedPixMap.save('test.jpg', 'jpg')

            if self.onSnippingCompleted is not None:
                self.onSnippingCompleted(grabbedPixMap)
            self.close()

    def start(self):
        # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        self.show()

    # def Pixmap_to_Opencv(self,qtpixmap):
    #     import cv2
    #     import numpy as np
    #     print('-----QPixmap_to_Opencv-----')
    #     print('qtpixmap type:',type(qtpixmap))
    #     qimg = qtpixmap.toImage()  # QPixmap-->QImage
    #     print('qimg type:', type(qimg))

    #     temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    #     temp_shape += (4,)
    #     ptr = qimg.bits()
    #     ptr.setsize(qimg.byteCount())
    #     result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    #     result = result[..., :3]
    #     cv2.imshow("result", result)
    #     if not cv2.imwrite('test.jpg',result):
    #         raise Exception("Could not write image")
    #     return result