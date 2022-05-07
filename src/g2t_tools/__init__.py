from enum import Enum
import os
from pathlib import Path
import pytesseract

# Scene Text Recognition Engine
class STR_Engine(Enum):
    PADDLE = 1
    EAST = 2

# Optical Character Recognition Engine
class OCR_Engine(Enum):
    MANGA_OCR = 1
    PADDLE_OCR = 2
    SPACE_OCR = 3
    GOOGLE_VISION = 4

bundle_dir = Path(os.path.dirname(os.path.abspath(__file__))).parents[1]
WIN_TESSERACT_DIR = Path(bundle_dir, "resources", "bin", "win", "tesseract")
path_to_tesseract = str(Path(WIN_TESSERACT_DIR, "tesseract.exe"))
paddle_models_path = str(Path(bundle_dir, "resources", "models", "paddleocr"))
manga_ocr_path =  str(Path(bundle_dir, "resources", "models", "manga-ocr-base"))