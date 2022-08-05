# Import libraries
from ppadb.client import Client
from time import sleep
from solve import solve
from utils import find_sudoku_board, get_cells, print_board, get_numbers, visualize_tap
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
print(f'Input "s" to solve sudoku\n>>> ', end='')
while input() == 's':
    print('Started solving, please don\'t touch the screen')
    
    # Get sudoku board
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)
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
    
    # Get numbers coords
    numbers = {}
    numbers = get_numbers(screen, sudoku_board, (x, y))
    
    if len(numbers) != 9:
        print('Could not find all numbers')
        continue
    
    # Send solved sudoku to device
    for col in range(9):
        for line in range(9):
            if cells[col][line].value == 0:
                device.shell(f'input tap {cells[col][line].x} {cells[col][line].y}')
                n_pos = numbers[sudoku_solved[line][col]]
                device.shell(f'input tap {n_pos[0]} {n_pos[1]}')
    
    print('Solved!, input "s" to solve another sudoku\n>>> ', end='')