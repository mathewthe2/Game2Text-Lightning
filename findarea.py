import mss
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import numpy as np
from PIL import Image
import cv2

def show_image(image):
    cv2.imshow('window', image)
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 

def get_screenshot():
    with mss.mss() as sct:
        # Get rid of the first, as it represents the "All in One" monitor:
        for num, monitor in enumerate(sct.monitors[1:], 1):
            # Get raw pixels from the screen
            sct_img = sct.grab(monitor)

            # Create the Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            open_cv_image = np.array(img) 
            # Convert RGB to BGR 
            open_cv_image = open_cv_image[:, :, ::-1].copy() 
            return open_cv_image

# https://github.com/sanifalimomin/Text-Detection-Using-OpenCV/blob/main/Text%20Detection%20Using%20OpenCV.ipynb
def get_boxes(image):
    # image height and width should be multiple of 32
    imgWidth=320
    imgHeight=320

    orig = image.copy()
    (H, W) = image.shape[:2]
    (newW, newH) = (imgWidth, imgHeight)

    rW = W / float(newW)
    rH = H / float(newH)
    image = cv2.resize(image, (newW, newH))

    (H, W) = image.shape[:2]
    
    # load model 
    net = cv2.dnn.readNet("resources/models/frozen_east_text_detection.pb")
    
    # create blob from image
    # blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
    #                          (123.68, 116.78, 103.94), swapRB=True, crop=False)
    
    # add layers for network
    outputLayers = []
    outputLayers.append("feature_fusion/Conv_7/Sigmoid")
    outputLayers.append("feature_fusion/concat_3")

    start = time.time()

    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                            (123.68, 116.78, 103.94), swapRB=True, crop=False)

    # Pass Input to Network and get the Ouput based on layers 
    net.setInput(blob)
    output = net.forward(outputLayers)
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

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)


    show_image(orig)

    

img = get_screenshot()
get_boxes(img)
