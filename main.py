import pygame
import random

BOARD_SIZE_X = 25
BOARD_SIZE_Y = 25
BOARD_SPACE_SIZE = 20

PLAYER1_START_X = 12
PLAYER1_START_Y = 12

COBRA_START_DIRECTION = "Up"

SEGMENT_SIZE = 20

# Define the objects that can occupy board spaces.
EMPTY = 0
COBRA = 1
FOOD = 2

EMPTY_RECT = pygame.Rect(0, 0, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE)
COBRA_RECT = pygame.Rect(0, 0, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE)
FOOD_RECT = pygame.Rect(0, 0, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE)

RED = (0xFF, 0x00, 0x00)
YELLOW = (0xFF, 0xFF, 0x00)
BLACK = (0x00, 0x00, 0x00)

class board(object):
    foodOnBoard = False
    def __init__(self, width, height, spaceSize):
        self.width = width
        self.height = height
        self.spaceSize = spaceSize
        self.spaces = [[0 for y in range(0, BOARD_SIZE_X)] for x in range(0, BOARD_SIZE_Y)]
    class cobra(object):
        numberOfSegments = 1
        sizeOfSegments = SEGMENT_SIZE
        posX = PLAYER1_START_X
        posY = PLAYER1_START_Y
        direction = COBRA_START_DIRECTION
        segments = []

class segment(object):
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

def draw_board(board):
    for y in range(0, BOARD_SIZE_Y):
        for x in range(0, BOARD_SIZE_X):
            drawX = x * BOARD_SPACE_SIZE
            drawY = y * BOARD_SPACE_SIZE
            if board.spaces[x][y] == COBRA:
                pygame.draw.rect(screen, RED, pygame.Rect(drawX, drawY, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE))
            elif board.spaces[x][y] == FOOD:
                pygame.draw.rect(screen, YELLOW, pygame.Rect(drawX, drawY, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE))
            elif board.spaces[x][y] == EMPTY:
                pygame.draw.rect(screen, BLACK, pygame.Rect(drawX, drawY, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE))

def create_food(board):
    x = random.randint(0, BOARD_SIZE_X - 1)
    y = random.randint(0, BOARD_SIZE_Y - 1)
    board.spaces[x][y] = FOOD

def update_segments(board):
    posX = board.cobra.posX
    posY = board.cobra.posY
    if board.spaces[posX][board.cobra.posY] == FOOD:
        board.cobra.segments.append(segment(board.cobra.posX, board.cobra.posY))
        board.foodOnBoard = False
    for seg in board.cobra.segments:
        prevPosX = seg.posX
        prevPosY = seg.posY
        board.spaces[prevPosX][prevPosY] = EMPTY
        seg.posX = posX
        seg.posY = posY
        board.spaces[seg.posX][seg.posY] = COBRA
        posX = prevPosX
        posY = prevPosY

def move_cobra(board):
    collision = False
    if board.cobra.direction == "Up":
        board.cobra.posY -= 1
    if board.cobra.direction == "Down":
        board.cobra.posY += 1
    if board.cobra.direction == "Left":
        board.cobra.posX -= 1
    if board.cobra.direction == "Right":
        board.cobra.posX += 1
    if (board.cobra.posX < 0) or (board.cobra.posY < 0) or (board.cobra.posX > BOARD_SIZE_X - 1)\
    or (board.cobra.posX > BOARD_SIZE_Y - 1) or (board.spaces[board.cobra.posX][board.cobra.posY] == COBRA):
        collision = True
    update_segments(board)
    return collision

def update_board(board):
    board.spaces[board.cobra.posX][board.cobra.posY] = EMPTY
    collision = move_cobra(board)
    return collision

# Set board size, cobra starting position, create first cobra segment, and initialize display
board1 = board(BOARD_SIZE_X, BOARD_SIZE_Y, BOARD_SPACE_SIZE)
#board1.cobra.posX = PLAYER1_START_X
#board1.cobra.posY = PLAYER1_START_Y
board1.cobra.segments.append(segment(board1.cobra.posX, board1.cobra.posY))

pygame.init()
screen = pygame.display.set_mode((500, 500))

gameRunning = True

while gameRunning == True:
    if not board1.foodOnBoard:
        create_food(board1)
        board1.foodOnBoard = True

    collision = update_board(board1)
    if collision == True:
        gameRunning = False

    draw_board(board1)
    pygame.display.update()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                board1.cobra.direction = "Up"
            if event.key == pygame.K_DOWN:
                board1.cobra.direction = "Down"
            if event.key == pygame.K_LEFT:
                board1.cobra.direction = "Left"
            if event.key == pygame.K_RIGHT:
                board1.cobra.direction = "Right"
    pygame.time.wait(100)