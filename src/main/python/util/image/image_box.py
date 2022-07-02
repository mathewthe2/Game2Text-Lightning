import numpy as np

class ImageBox():

    def __init__(self, box, image):
        self.box = box
        self.relative_box = box # pre-adjustment coordiantes
        self.image = image # PIL Image

    def is_similar(self, candidate_box):
        # cutoff = 2
        # return cutoff > abs(dhash(self.image) - dhash(candidate_image.image)) 
        np_image = np.asarray(self.image)
        np_candidate =  np.asarray(candidate_box.image)
        return np_image.shape == np_candidate.shape and not(np.bitwise_xor(np_image,np_candidate).any())
