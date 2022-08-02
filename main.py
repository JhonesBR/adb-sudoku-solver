# Variables
SUDOKU_COORDINATES = (15, 450, 1060, 1490) # (left, top, right, bottom)
SUDOKU_WIDTH = SUDOKU_COORDINATES[2] - SUDOKU_COORDINATES[0]
SUDOKU_HEIGHT = SUDOKU_COORDINATES[3] - SUDOKU_COORDINATES[1]
CELL_WIDTH = SUDOKU_WIDTH / 9
CELL_HEIGHT = SUDOKU_HEIGHT / 9

# Import libraries
from ppadb.client import Client
from PIL import Image
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

    image = Image.open('screen.png')
    image = image.crop(SUDOKU_COORDINATES)
    image.save('sudoku.png')

    OFFSET = int((CELL_WIDTH+CELL_HEIGHT) / 2 * 0.05)
    board = []
    for x in range(9):
        line = []
        for y in range(9):
            left = x * CELL_WIDTH + OFFSET
            top = y * CELL_HEIGHT + OFFSET
            right = left + CELL_WIDTH - OFFSET
            bottom = top + CELL_HEIGHT - OFFSET
            line.append(image.crop((left, top, right, bottom)))
        board.append(line)

    for i in range(len(board)):
        for j in range(len(board)):
            board[i][j].save(f'cells/{i}_{j}.png')