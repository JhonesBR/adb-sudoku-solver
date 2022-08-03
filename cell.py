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
        img = cv2.resize(np.array(self.image.copy().convert('L')), (64, 64))
        img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
        
        if mean(img)[0] >= 253:
            self.value = 0
            return
        
        _, thresh = cv2.threshold(img, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(img)
        cv2.drawContours(mask, contours, 0, 255, -1)
        out = np.zeros_like(img)
        out[mask == 255] = img[mask == 255]
        
        self.value  = pytesseract.image_to_string(out, config='--psm 10 --oem 3 -c tessedit_char_whitelist=" 123456789"')
        if self.value.strip() == '' or not self.value.strip().isdigit():
            self.value = '0' # Assume 0 if no value is found
        else:
            self.value = int(self.value)