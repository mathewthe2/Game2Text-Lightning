from enum import Enum
import os
from pathlib import Path
import pytesseract

# Scene Text Recognition Engine
class STR_Engine(Enum):
    EAST = 1

# Optical Character Recognition Engine
class OCR_Engine(Enum):
    TESSERACT_DEFAULT = 1
    TESSERACT_LSTM = 2
    MANGA_OCR = 3
    SPACE_OCR = 4
    GOOGLE_VISION = 5

bundle_dir = Path(os.path.dirname(os.path.abspath(__file__))).parents[1]
WIN_TESSERACT_DIR = Path(bundle_dir, "resources", "bin", "win", "tesseract")
path_to_tesseract = str(Path(WIN_TESSERACT_DIR, "tesseract.exe"))