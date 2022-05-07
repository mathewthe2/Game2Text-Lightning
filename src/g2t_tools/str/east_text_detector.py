# from PIL import Image
from imutils.object_detection import non_max_suppression
import numpy as np
import time
import cv2
from .cropped_image import CroppedImage

class East_Text_Detector():
    def __init__(self, image=None, padding=5):
        self.image = image
        self.rW = 0 # width ratio for cnn
        self.rH = 0 # height ratio for cnn
        self.net = None
        self.outputLayers = []
        self.load_model()

    def load_model(self):
        self.net = cv2.dnn.readNet("resources/models/frozen_east_text_detection.pb")
        # add layers for network
        self.outputLayers.append("feature_fusion/Conv_7/Sigmoid")
        self.outputLayers.append("feature_fusion/concat_3")

    # https://github.com/sanifalimomin/Text-Detection-Using-OpenCV/blob/main/Text%20Detection%20Using%20OpenCV.ipynb
    def detect(self):
        image = self.image.copy()
        # image height and width should be multiple of 32
        imgWidth=320
        imgHeight=320

        # orig = image.copy()
        (H, W) = image.shape[:2]
        (newW, newH) = (imgWidth, imgHeight)

        self.rW = W / float(newW)
        self.rH = H / float(newH)
        image = cv2.resize(image, (newW, newH))

        (H, W) = image.shape[:2]
        
        start = time.time()
        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                (123.68, 116.78, 103.94), swapRB=True, crop=False)

        # Pass Input to Network and get the Ouput based on layers 
        self.net.setInput(blob)
        output = self.net.forward(self.outputLayers)
        scores = output[0]
        geometry = output[1]

        # Get rects and confidence score for bounding boxes

        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        for y in range(0, numRows):
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            for x in range(0, numCols):
                # if our score does not have sufficient probability, ignore it
                if scoresData[x] < 0.5:
                    continue

                # compute the offset factor as our resulting feature maps will
                # be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                # extract the rotation angle for the prediction and then
                # compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                # use the geometry volume to derive the width and height of
                # the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                # compute both the starting and ending (x, y)-coordinates for
                # the text prediction bounding box
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                # add the bounding box coordinates and probability score to
                # our respective lists
                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

        # apply non-maxima suppression to suppress weak, overlapping bounding
        boxes = non_max_suppression(np.array(rects), probs=confidences)
        
        end = time.time()
        print(end - start)
        return boxes

    def crop(self, box):
        return CroppedImage(self.image, self.rW, self.rH, box)
