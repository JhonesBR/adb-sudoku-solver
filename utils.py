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