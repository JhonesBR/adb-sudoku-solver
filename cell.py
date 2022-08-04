from re import S
from cv2 import mean
from skimage.metrics import structural_similarity
from PIL import Image
import numpy as np
import cv2
import pytesseract

PYTESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract'
pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH

class Cell:
    x:int = 0
    y:int = 0
    value:int = 0
    pos:tuple = (0,0)
    image:Image = None
    
    def __init__(self) -> None:
        pass
    
    def __repr__(self) -> str:
        return f'Cell({self.pos}), value={self.value})'
    
    def get_value(self) -> None:
        # Initial image processing
        img = cv2.resize(self.image , (200, 200))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
        
        # Empty image
        if mean(img)[0] >= 253:
            self.value = 0
            return
        
        # pytesseract preparation
        _, thresh = cv2.threshold(img, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(img)
        cv2.drawContours(mask, contours, 0, 255, -1)
        out = np.zeros_like(img)
        out[mask == 255] = img[mask == 255]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        close = cv2.morphologyEx(out, cv2.MORPH_CLOSE, kernel, iterations=2)
        blurred = cv2.GaussianBlur(close, (0,0), 3)
        sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharp = cv2.filter2D(blurred, -1, sharpen_filter)
        
        # Get value
        text = list(pytesseract.image_to_string(sharp, lang="eng",config='--psm 6 --oem 3 -c tessedit_char_whitelist=" 123456789"'))
        if len(text) == 0:
            self.value = 0
        else:
            self.value = int(text[0].strip())