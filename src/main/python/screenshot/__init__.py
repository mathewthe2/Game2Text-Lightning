import mss
import numpy as np
from PIL import Image
from enum import Enum

class Capture_Mode(Enum):
    WINDOW = 0
    DESKTOP_AREA = 1

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

def get_screenshot_image():
    with mss.mss() as sct:
    # Get rid of the first, as it represents the "All in One" monitor:
        for num, monitor in enumerate(sct.monitors[1:], 1):
            # Get raw pixels from the screen
            sct_img = sct.grab(monitor)

            # Create the Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            return img