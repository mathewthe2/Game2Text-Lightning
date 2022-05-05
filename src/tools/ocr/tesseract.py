import pytesseract
from pytesseract import Output
from .character import Character

class Tesseract():

    y_padding = 25 # detect box padding

    def __init__(self, path_to_tesseract):
        pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
        self.tesseract_language = 'jpn'
        self.oem = 3
        self.extra_options = "-c chop_enable=T -c use_new_state_cost=F -c segment_segcost_rating=F -c enable_new_segsearch=0 -c language_model_ngram_on=0 -c textord_force_make_prop_words=F -c edges_max_children_per_outline=40"

    def get_config(self):
        return r'--oem {} -c preserve_interword_spaces=1 {}'.format(self.oem, self.extra_options.strip('"'))

    def extract_text(self, image):
        text = pytesseract.image_to_string(image)
        return text

    def extract_boxed_characters(self, image, origin):
        height = image.shape[0]
        d = pytesseract.image_to_boxes(image, config=self.get_config(), lang=self.tesseract_language, output_type=Output.DICT)
        if 'char' not in d:
            return []
        n_boxes = len(d['char'])
        characters = []
        origin_x, origin_y = origin
        for i in range(n_boxes):
            (text,x1,y2,x2,y1) = (d['char'][i],d['left'][i],d['top'][i],d['right'][i],d['bottom'][i])
            print(text, '{}, {}'.format(x1, y1))
            # print(text, '{}, {}'.format(x1 + origin.x(), y1 + origin.y()))
            characters.append(Character(text, x1 + origin_x, x2 + origin_x, origin_y + height - y1 - self.y_padding, origin_y + height - y2 - self.y_padding, i))
        return characters