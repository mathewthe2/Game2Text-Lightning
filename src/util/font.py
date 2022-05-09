import ctypes

FONT_SIZE_C = 0.5 # constant to fit font size in pyqt label

def get_text_dimensions(text, points, font):
    class SIZE(ctypes.Structure):
        _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

    hdc = ctypes.windll.user32.GetDC(0)
    hfont = ctypes.windll.gdi32.CreateFontA(points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
    hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

    size = SIZE(0, 0)
    ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

    ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
    ctypes.windll.gdi32.DeleteObject(hfont)

    return (size.cx, size.cy)

def get_font_size(s, font_style, w, h):
    i = 1
    x, y = get_text_dimensions(s, i, font_style)
    while x < w and y < h:
        i += 1
        x, y = get_text_dimensions(s, i, font_style)
    return FONT_SIZE_C*(i-1)

# print(get_font_size("家のお使いだったから", 'Times', 100, 50))