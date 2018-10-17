import pygame
import random

BOARD_SIZE_WIDTH = 25
BOARD_SIZE_HEIGHT = 25

# This will determine the size of the objects drawn on the board.
# Must be equal to resolution
BOARD_SPACE_SIZE = 20

DISPLAY_RESOLUTION_WIDTH = BOARD_SIZE_WIDTH * BOARD_SPACE_SIZE
DISPLAY_RESOLUTION_HEIGHT = BOARD_SIZE_HEIGHT * BOARD_SPACE_SIZE

PLAYER1_START_X = 12
PLAYER1_START_Y = 12

COBRA_START_DIRECTION = "Up"
# Number of milliseconds between player movements.
MOVEMENT_DELAY = 100

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
        self.spaces = [[0 for y in range(0, BOARD_SIZE_HEIGHT)] for x in range(0, BOARD_SIZE_WIDTH)]

    def create_food(self):
        while self.foodOnBoard == False:
            x = random.randint(0, BOARD_SIZE_WIDTH - 1)
            y = random.randint(0, BOARD_SIZE_HEIGHT - 1)
            if self.spaces[x][y] == EMPTY:
                self.spaces[x][y] = FOOD
                self.foodOnBoard = True

    def draw_board(self, screen):
        for y in range(0, BOARD_SIZE_HEIGHT):
            for x in range(0, BOARD_SIZE_WIDTH):
                drawX = x * BOARD_SPACE_SIZE
                drawY = y * BOARD_SPACE_SIZE
                if self.spaces[x][y] == COBRA:
                    pygame.draw.rect(screen, RED, pygame.Rect(drawX, drawY, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE))
                elif self.spaces[x][y] == FOOD:
                    pygame.draw.rect(screen, YELLOW, pygame.Rect(drawX, drawY, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE))
                elif self.spaces[x][y] == EMPTY:
                    pygame.draw.rect(screen, BLACK, pygame.Rect(drawX, drawY, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE))
    
class cobra(object):
    numberOfSegments = 1
    sizeOfSegments = SEGMENT_SIZE
    segments = []
    
    def __init__(self, posX, posY, direction):
        self.posX = posX
        self.posY = posY
        self.direction = direction
        
    class segment(object):
        def __init__(self, posX, posY):
            self.posX = posX
            self.posY = posY

    def add_segment(self, segment):
        self.segments.append(segment)

    def move(self):
        if self.direction == "Up":
            self.posY -= 1
        if self.direction == "Down":
            self.posY += 1
        if self.direction == "Left":
            self.posX -= 1
        if self.direction == "Right":
            self.posX += 1    

def check_collision(board, cobra):
    if (cobra.posX < 0) or (cobra.posY < 0) or (cobra.posX > BOARD_SIZE_WIDTH - 1)\
    or (cobra.posY > BOARD_SIZE_HEIGHT - 1) or (board.spaces[cobra.posX][cobra.posY] == COBRA):
        collision = True
    else:
        collision = False

    return collision

def update_segments(board, cobra):
    posX = cobra.posX
    posY = cobra.posY

    if board.spaces[posX][posY] == FOOD:
        cobra.add_segment(cobra.segment(posX, posY))
        board.foodOnBoard = False

    for seg in cobra.segments:
        prevPosX = seg.posX
        prevPosY = seg.posY
        board.spaces[prevPosX][prevPosY] = EMPTY
        seg.posX = posX
        seg.posY = posY
        board.spaces[seg.posX][seg.posY] = COBRA
        posX = prevPosX
        posY = prevPosY

def main():
    # Set board size, cobra starting position, create first cobra segment, and initialize display
    board1 = board(BOARD_SIZE_WIDTH, BOARD_SIZE_HEIGHT, BOARD_SPACE_SIZE)
    cobra1 = cobra(PLAYER1_START_X, PLAYER1_START_Y, COBRA_START_DIRECTION)
    cobra1.add_segment(cobra.segment(cobra1.posX, cobra1.posY))

    pygame.init()

    screen = pygame.display.set_mode((DISPLAY_RESOLUTION_WIDTH, DISPLAY_RESOLUTION_HEIGHT))

    gameRunning = True
    paused = False

    while gameRunning == True:

        update_segments(board1, cobra1)
        board1.draw_board(screen)
        pygame.display.update()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cobra1.direction = "Up"
                if event.key == pygame.K_DOWN:
                    cobra1.direction = "Down"
                if event.key == pygame.K_LEFT:
                    cobra1.direction = "Left"
                if event.key == pygame.K_RIGHT:
                    cobra1.direction = "Right"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    if not paused:
                        paused = True
                    else:
                        paused = False

        if not paused:
            cobra1.move()
            collision = check_collision(board1, cobra1)

            if not board1.foodOnBoard:
                board1.create_food()

            if collision == True:
                gameRunning = False

            pygame.time.wait(MOVEMENT_DELAY)

main()