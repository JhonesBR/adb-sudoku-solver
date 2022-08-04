# Import libraries
from ppadb.client import Client
from time import sleep
from solve import solve
from utils import find_sudoku_board, get_cells, print_board
import cv2
import os

# Ensure adb is initalized
os.system('adb start-server')

# Connect to device
adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()

# Ensure device is connected
if len(devices) == 0:
    print("No devices found")
    exit()

# Connect to device and start loop
device = devices[0]
print('Connected to device: ' + device.serial)
print(f'Input "s" to solve sudoku')
while input() == 's':
    print('Started solving, please don\'t touch the screen')
    
    # Get sudoku board
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)

    # Get sudoku board
    screen = cv2.imread("screen.png")
    sudoku_board, (x, y) = find_sudoku_board(screen)

    # Get individual cells
    cells = get_cells(sudoku_board, (x, y))
    sudoku_matrix = []
    for line in range(9):
        sudoku_line = []
        for col in range(9):
            # Get cell value using pytesseract
            cells[col][line].get_value()
            sudoku_line.append(cells[col][line].value)
        sudoku_matrix.append(sudoku_line)
        

    # Solve sudoku
    print('\nOriginal:')
    print_board(sudoku_matrix)
    sudoku_solved = solve(sudoku_matrix)
    print('\nSolved:')
    print_board(sudoku_solved)
    
    # Send solved sudoku to device
    for col in range(9):
        for line in range(9):
            if cells[col][line].value == 0:
                device.shell(f'input tap {cells[col][line].x} {cells[col][line].y}')
                # TODO: input number
    
    print('Solved!, input "s" to solve another sudoku')