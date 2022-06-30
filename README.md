# Game2Text-Lightning
Experimental OCR for language learning.


## Windows development setup

Set up virtual environment. 

**Python 3.6.8** is recommended. Packager FBS requires 3.5 or 3.6 to work.

```bash
virtualenv venv --python=python3.6
call venv/scripts/activate.bat
```

Install.

```bash
pip install -r requirements/windows.txt
```

Run.

```bash
fbs run
```

Package.

To package, (Visual C++ Redistributable for Visual Studio 2012)[https://www.microsoft.com/en-us/download/details.aspx?id=30679] is required. Install, then add the directory *C:\Windows\SysWOW64* to PATH (Windows environment variables).

```bash
fbs freeze
```

### Before packaging:

Note: make sure you have installed pyinstaller version 4.0 or higher.

Edit paddle\dataset\image.py.

Comment out code block that starts with "if six.PY3" and add the following code block underneath.

```python
try:
    import cv2
except ImportError
    cv2 = None
import os
```

Prefix paddle modules with **paddleocr.** in *paddleocr/paddleocr.py*.

```python
tools = importlib.import_module('.', 'paddleocr.tools')
ppocr = importlib.import_module('.', 'paddleocr.ppocr')
ppstructure = importlib.import_module('.', 'paddleocr.ppstructure')

from paddleocr.tools.infer import predict_system
from paddleocr.ppocr.utils.logging import get_logger

logger = get_logger()
from paddleocr.ppocr.utils.utility import check_and_read_gif, get_image_file_list
from paddleocr.ppocr.utils.network import maybe_download, download_with_progressbar, is_link, confirm_model_dir_url
from paddleocr.tools.infer.utility import draw_ocr, str2bool, check_gpu
from paddleocr.ppstructure.utility import init_args, draw_structure_result
from paddleocr.ppstructure.predict_system import StructureSystem, save_structure_res
```

Prefix imports for all files under the *paddleocr/tools/infer* subdirectory, including *predict_system.py*, *predict_cls.py* etc...

Prefix imports for files in **data**, **postprocess**, **ppstructure**, **tools/infer**, and **ppocr\data\imaug** folders. You will probably have to run *fbs freeze --debug* to know which imports are missing.

Fix imports for *paddleocr\ppocr\utils\e2e_utils\pgnet_pp_utils.py*.

```python
# __dir__ = os.path.dirname(__file__)
# sys.path.append(__dir__)
# sys.path.append(os.path.join(__dir__, '..'))
from paddleocr.ppocr.utils.e2e_utils.extract_textpoint_slow import *
from paddleocr.ppocr.utils.e2e_utils.extract_textpoint_fast import generate_pivot_list_fast, restore_poly
```

## Acknowledgments
- JMDict
- Paddle OCR
- Rikaichan