import pytesseract
from pytesseract import Output
import cv2
import os
from pathlib import Path
from character import Character

bundle_dir = os.path.dirname(os.path.abspath(__file__))
WIN_TESSERACT_DIR = Path(bundle_dir, "resources", "bin", "win", "tesseract")
path_to_tesseract = str(Path(WIN_TESSERACT_DIR, "tesseract.exe"))
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

tesseract_language = 'jpn'
oem = 3
extra_options = "-c chop_enable=T -c use_new_state_cost=F -c segment_segcost_rating=F -c enable_new_segsearch=0 -c language_model_ngram_on=0 -c textord_force_make_prop_words=F -c edges_max_children_per_outline=40"
custom_config = r'--oem {} -c preserve_interword_spaces=1 {}'.format(oem, extra_options.strip('"'))

y_padding = 25
# img = cv2.imread('temp.jpg')

# def draw_big():
#     d = pytesseract.image_to_data(img, config=custom_config, lang=tesseract_language, output_type=Output.DICT)
#     n_boxes = len(d['level'])
#     print(n_boxes)
#     for i in range(n_boxes):
#         (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     cv2.imshow('img', img)
#     cv2.waitKey(0)


def draw_character(origin, end):
    height = img.shape[0]
    width = img.shape[1]

    d = pytesseract.image_to_boxes(img, config=custom_config, lang=tesseract_language, output_type=Output.DICT)
    if 'char' not in d:
        return []
    n_boxes = len(d['char'])
    characters = []
    for i in range(n_boxes):
        (text,x1,y2,x2,y1) = (d['char'][i],d['left'][i],d['top'][i],d['right'][i],d['bottom'][i])
        print(text, '{}, {}'.format(x1 + origin.x(), y1 + origin.y()))
        # characters.append(Character(text, x1 + origin.x(), x2 + origin.x(), y1 + origin.y(), y2+origin.y(), i))
        characters.append(Character(text, x1 + origin.x(), x2 + origin.x(), origin.y() + height - y1 - y_padding, origin.y() + height - y2 - y_padding, i))
        # cv2.rectangle(img, (x1,height-y1), (x2,height-y2) , (0,255,0), 2)
    # cv2.imshow('img',img)
    # cv2.waitKey(0)
    return characters
    
def show_image(image_numpy_data, origin, end):
    global img
    img = image_numpy_data
    print(type(img))
    return draw_character(origin, end)