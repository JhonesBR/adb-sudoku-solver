# Import liberies
import cv2
from cell import Cell

def find_sudoku_board(img):
    # Process image
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_img, 160, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    
    # Define min area based on original image and define sudoku_image
    min_area = img.shape[0] * img.shape[1] * 0.4
    sudoku_image = None
    
    # Get sudoku image based on contours and min area
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area:
            x,y,w,h = cv2.boundingRect(c)
            sudoku_image = img[y:y+h,x:x+w]

    return sudoku_image, (x, y)

def get_cells(sudoku_img, sudoku_pos:tuple):
    # Find cells
    cell_height = sudoku_img.shape[0] // 9
    cell_width = sudoku_img.shape[1] // 9
    
    cells = [[Cell() for x in range(9)] for y in range(9)]
    offset = int((cell_height + cell_width / 2) * 0.1)
    for line in range(9):
        for col in range(9):
            x = col * cell_width + offset
            y = line * cell_height + offset
            h = cell_height - 2*offset
            w = cell_width - 2*offset
            cells[col][line].image = sudoku_img[y:y+h, x:x+w]
            cells[col][line].pos = (line, col)
            cells[col][line].x = int(sudoku_pos[0]+x + cell_width/2)
            cells[col][line].y = int(sudoku_pos[1]+y + cell_height/2)
            
    return cells

def print_board(board):
    for i in range(9):
        if i%3==0 :
                print("+",end="")
                print("-------+"*3)
        for j in range(9):
            if j%3 ==0 :
                print("",end="| ")
            print(int(board[i][j]),end=" ")
        print("",end="|")       
        print()
    print("+",end="")
    print("-------+"*3)
    
def get_numbers(screen, sudoku_board, sudoku_start_pos):
    # Crop image below sudoku board
    x, y = sudoku_start_pos[0], sudoku_start_pos[1]
    sudoku_end_pos = (x + sudoku_board.shape[1], y + sudoku_board.shape[0])
    img = screen[y+sudoku_board.shape[0]:,:]
    
    # Image processing
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imt_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(imt_thresh, kernel, iterations=1)
    cnts, hier = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # Get 9 elements at same line
    elements_y = {}
    thresh = int(img.shape[0] * 0.01)
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        keys = list(elements_y.keys())
        for key in keys:
            if abs(y - key) < thresh:
                elements_y[key] += 1
                continue
        else:
            if y not in keys:
                elements_y[y] = 1
    
    # Find numbers
    img2 = img.copy()
    numbers_pos = []
    for element in elements_y:
        if elements_y[element] == 9:
            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)
                if abs(y - element) < thresh:
                    cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img2, str(y), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    numbers_pos.append((int(x+w/2), int(sudoku_end_pos[1]+y+h/2)))

    # Order numbers by x position and make dict
    numbers_ordered = sorted(numbers_pos, key=lambda x: x[0])
    numbers = {i+1:numbers_ordered[i] for i in range(len(numbers_ordered))}
    
    return numbers

# Used to visualize screen touch
def visualize_tap(screen, x, y):
    img = screen.copy()
    cv2.rectangle(img, (x-20, y-20), (x+20, y+20), (0, 255, 0), 2)
    img = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()