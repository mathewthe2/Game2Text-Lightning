import numpy as np
import cv2
from PIL import Image
from enum import Enum

class IMAGE_TYPE(Enum):
    CV = 1
    PIL = 2
    NP = 3

class ImageObject():
    def __init__(self, image, type=IMAGE_TYPE.PIL):
        self.image = image if type == IMAGE_TYPE.PIL else self.cv_to_pil(image)

    def get_image(self, type=IMAGE_TYPE.PIL):
        if type == IMAGE_TYPE.PIL:
            return self.image
        elif type == IMAGE_TYPE.NP:
            return np.asarray(self.image)
        elif type == IMAGE_TYPE.CV:
            open_cv_image = np.array(self.image.convert('RGB')) 
            # Convert RGB to BGR 
            return open_cv_image[:, :, ::-1].copy() 

    def cv_to_pil(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(image)