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
    image:np.array = None
    
    def __init__(self) -> None:
        pass
    
    def __repr__(self) -> str:
        return f'Cell({self.pos}), value={self.value})'
    
    def get_value(self) -> None:
        # Image processing
        img = self.image.copy()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, imt_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        
        # Empty image
        if cv2.mean(imt_thresh)[0] >= 253:
            self.value = 0
            return
        
        # pytesseract preparation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
        dilation = cv2.dilate(imt_thresh, kernel, iterations=1)
        cnts, hier = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(cnts) == 0:
            self.value = 0
            return
        else:
            # Found number
            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)
                cropped = imt_thresh[y:y+h, x:x+w]
                cropped = cv2.bitwise_not(cropped)
        
        # Get value
        text = list(pytesseract.image_to_string(cropped, lang="eng",config='--psm 6 --oem 3 -c tessedit_char_whitelist=" 123456789"'))
        if len(text) == 0:
            self.value = 0
        else:
            self.value = int(text[0].strip())