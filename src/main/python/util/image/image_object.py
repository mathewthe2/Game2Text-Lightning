import numpy as np
from PIL import Image
import base64
from io import BytesIO
from . import IMAGE_TYPE

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
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(image)

    def base_64(self):
        buffered = BytesIO()
        self.image.save(buffered, format="JPEG")
        img_byte = buffered.getvalue()
        return  base64.b64encode(img_byte).decode()