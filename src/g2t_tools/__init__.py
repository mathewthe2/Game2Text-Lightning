from enum import Enum
import os
from pathlib import Path

# Optical Character Recognition Engine
class OCR_Engine(Enum):
    PADDLE_OCR = 1
    SPACE_OCR = 2
    GOOGLE_VISION = 3

bundle_dir = Path(os.path.dirname(os.path.abspath(__file__))).parents[1]
paddle_models_path = str(Path(bundle_dir, "resources", "models", "paddleocr"))