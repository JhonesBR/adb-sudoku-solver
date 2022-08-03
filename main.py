# Variables
SUDOKU_COORDINATES = (15, 450, 1060, 1490) # (left, top, right, bottom)
SUDOKU_WIDTH = SUDOKU_COORDINATES[2] - SUDOKU_COORDINATES[0]
SUDOKU_HEIGHT = SUDOKU_COORDINATES[3] - SUDOKU_COORDINATES[1]
CELL_WIDTH = SUDOKU_WIDTH / 9
CELL_HEIGHT = SUDOKU_HEIGHT / 9

# Import libraries
import numpy as np
from ppadb.client import Client
from solve import solve
from PIL import Image
from cell import Cell
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
    # Get sudoku board
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)

    # Get sudoku board
    image = Image.open('screen.png')
    image = image.crop(SUDOKU_COORDINATES)

    # Get individual cells
    OFFSET = int((CELL_WIDTH+CELL_HEIGHT) / 2 * 0.1)
    board = []
    for line in range(9):
        lineList = []
        for col in range(9):
            cell = Cell()
            
            # Define cell position in sudoku
            cell.pos = (line, col)
            
            # Define cell position in screen
            cell.x = SUDOKU_COORDINATES[0] + col * CELL_WIDTH + (CELL_WIDTH / 2)
            cell.y = SUDOKU_COORDINATES[1] + line * CELL_HEIGHT + (CELL_HEIGHT / 2)
            
            # Get cell image
            left = col * CELL_WIDTH + OFFSET
            top = line * CELL_HEIGHT + OFFSET
            right = left + CELL_WIDTH - OFFSET
            bottom = top + CELL_HEIGHT - OFFSET
            img = image.crop((left, top, right, bottom)).resize((64, 64))
            img = img.convert('L')
            cell.image = img
            
            # Get cell value using pytesseract
            cell.get_value()
            
            lineList.append(cell)
        board.append(lineList)
        
    # Solve sudoku
    boardValue = [[int(e.value) for e in line] for line in board]
    print('\Original:')
    for line in boardValue:
        print(line)
    boardSolved = solve(boardValue)
    print('\nSolved:')
    for line in boardSolved:
        print(line)