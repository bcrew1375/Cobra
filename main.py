import pygame
from random import randint

BOARD_SIZE_WIDTH = 25
BOARD_SIZE_HEIGHT = 25

# This will determine the size of the objects drawn on the board.
# Must be equal to resolution
BOARD_SPACE_SIZE = 20

DISPLAY_RESOLUTION_WIDTH = BOARD_SIZE_WIDTH * BOARD_SPACE_SIZE
DISPLAY_RESOLUTION_HEIGHT = BOARD_SIZE_HEIGHT * BOARD_SPACE_SIZE

PLAYER1_START_X = 10
PLAYER1_START_Y = 12

OPPONENT_ON = True

OPPONENT_START_X = 14
OPPONENT_START_Y = 12

# This will determine how long the opponent takes to acquire a new food target.
# Raising it will give the player more time to respond to new food appearing.
OPPONENT_TURNS_TO_WAIT = 4

COBRA_START_DIRECTION = "Up"
# Number of milliseconds between player movements.
MOVEMENT_DELAY = 100

SEGMENT_SIZE = 20

# Define the objects that can occupy board spaces.
EMPTY_SPACE = 0
COBRA1_SPACE = 1
COBRA2_SPACE = 2
FOOD_SPACE = 3

RED = (0xFF, 0x00, 0x00)
YELLOW = (0xFF, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0xFF)
BLACK = (0x00, 0x00, 0x00)

class Food(object):
    def __init__(self, posX, posY, index):
        self.posX = posX
        self.posY = posY
        self.index = index

class Board(object):
    foodOnBoard = False
    amountOfFood = 0

    def __init__(self, width, height, spaceSize):
        self.width = width
        self.height = height
        self.spaceSize = spaceSize
        self.spaces = [[0 for y in range(0, BOARD_SIZE_HEIGHT)] for x in range(0, BOARD_SIZE_WIDTH)]
        self.foodList = []

    def create_food(self):
        while self.foodOnBoard == False:
            x = randint(0, BOARD_SIZE_WIDTH - 1)
            y = randint(0, BOARD_SIZE_HEIGHT - 1)
            if self.spaces[x][y] == EMPTY_SPACE:
                self.spaces[x][y] = FOOD_SPACE
                self.amountOfFood += 1
                foodIndex = self.amountOfFood - 1
                self.foodList.append(Food(x, y, foodIndex))
                self.foodOnBoard = True

    def draw_board(self, screen):
        for y in range(0, BOARD_SIZE_HEIGHT):
            for x in range(0, BOARD_SIZE_WIDTH):
                drawX = x * BOARD_SPACE_SIZE
                drawY = y * BOARD_SPACE_SIZE

                space_object = self.spaces[x][y]

                if space_object == COBRA1_SPACE:
                    color = RED
                elif space_object == COBRA2_SPACE:
                    color = BLUE
                elif space_object == FOOD_SPACE:
                    color = YELLOW
                elif space_object == EMPTY_SPACE:
                    color = BLACK

                pygame.draw.rect(screen, color, pygame.Rect(drawX, drawY, BOARD_SPACE_SIZE, BOARD_SPACE_SIZE))
    
class Cobra(object):
    segmentsToAdd = 1
    sizeOfSegments = SEGMENT_SIZE
    
    def __init__(self, posX, posY, direction, spaceType):
        self.posX = posX
        self.posY = posY
        self.direction = direction
        self.spaceType = spaceType
        self.segments = []
        collision = False
        
    class Segment(object):
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

class Opponent(Cobra):
    turnsToWait = OPPONENT_TURNS_TO_WAIT

    def __init__(self, posX, posY, direction, spaceType):
        # This will hold the currently targeted piece of food's location.
        self.target = Food(-1, -1, -1)
        self.posX = posX
        self.posY = posY
        self.direction = direction
        self.spaceType = spaceType
        self.segments = []
        collision = False

    def get_food_target(self, board):
        if board.foodOnBoard == True:
            prevDistance = -1
            distance = -1

            for food in board.foodList:
                # Determine the food's distance from the current position.
                distance = abs(food.posX - self.posX) + abs(food.posY - self.posY)
                
                if prevDistance == -1:
                    self.target = food
                elif prevDistance > distance:
                    self.target = food

                prevDistance = distance
            
            #print (self.target.posX, self.target.posY)

    def check_target(self, board):
        # See if the currently targeted piece of food is gone.
        # A negative value will indicate that a target is not set.
        if board.spaces[self.target.posX][self.target.posY] != FOOD_SPACE:
            self.target = Food(-1, -1, -1)

    def set_direction(self, board):
        # Check if the target food is closer horizontally or vertically.
        horizontalDistance = abs(self.posX - self.target.posX)
        verticalDistance = abs(self.posY - self.target.posY)

        if horizontalDistance > verticalDistance:

            # If the target food is to the left.
            if self.posX > self.target.posX:
                # Make sure the opponent isn't about to run into a barrier.
                if board.spaces[self.posX - 1][self.posY] != COBRA1_SPACE and\
                   board.spaces[self.posX - 1][self.posY] != COBRA2_SPACE:
                    # If the opponent would turn back on itself, it needs to move up or down before going left.
                    if self.direction == "Right":
                        if self.posY > self.target.posY:
                            self.direction = "Up"
                        else:
                            self.direction = "Down"
                    else:
                        self.direction = "Left"
                # If there is an obstacle, look for an empty spot to move to.
                else:
                    if board.spaces[self.posX][self.posY - 1] == EMPTY_SPACE\
                    and self.posY > self.target.posY:
                        self.direction = "Up"
                    elif board.spaces[self.posX][self.posY + 1] == EMPTY_SPACE\
                    and self.posY <= self.target.posY:
                        self.direction = "Down"
                    elif board.spaces[self.posX - 1][self.posY] == EMPTY_SPACE:
                        self.direction = "Right"

            # If the target food is to the right.
            else:
                # Make sure the opponent isn't about to run into a barrier.
                if board.spaces[self.posX + 1][self.posY] != COBRA1_SPACE and\
                   board.spaces[self.posX + 1][self.posY] != COBRA2_SPACE:
                    # If the opponent would turn back on itself, it needs to move up or down before going right.
                    if self.direction == "Left":
                        if self.posY > self.target.posY:
                            self.direction = "Up"
                        else:
                            self.direction = "Down"
                    else:
                        self.direction = "Right"
                # If there is an obstacle, look for an empty spot to move to.
                else:
                    if board.spaces[self.posX][self.posY - 1] == EMPTY_SPACE\
                    and self.posY > self.target.posY:
                        self.direction = "Up"
                    elif board.spaces[self.posX][self.posY + 1] == EMPTY_SPACE\
                    and self.posY <= self.target.posY:
                        self.direction = "Down"
                    elif board.spaces[self.posX - 1][self.posY] == EMPTY_SPACE:
                        self.direction = "Left"
        else:

            # If the target food is up.
            if self.posY > self.target.posY:
                # Make sure the opponent isn't about to run into itself or the player.
                if board.spaces[self.posX][self.posY - 1] != COBRA1_SPACE and\
                   board.spaces[self.posX][self.posY - 1] != COBRA2_SPACE:
                    # If the opponent would turn back on itself, it needs to move left or right before going up.
                    if self.direction == "Down":
                        if self.posX > self.target.posX:
                            self.direction = "Left"
                        else:
                            self.direction = "Right"
                    else:
                        self.direction = "Up"
                # If there is an obstacle, look for an empty spot to move to.
                else:
                    if board.spaces[self.posX - 1][self.posY] == EMPTY_SPACE\
                    and self.posX > self.target.posX:
                        self.direction = "Left"
                    elif board.spaces[self.posX + 1][self.posY] == EMPTY_SPACE\
                    and self.posX <= self.target.posX:
                        self.direction = "Right"
                    elif board.spaces[self.posX][self.posY + 1] == EMPTY_SPACE:
                        self.direction = "Down"

            # If the target food is down.
            else:
                # Make sure the opponent isn't about to run into a barrier.
                if board.spaces[self.posX][self.posY + 1] != COBRA1_SPACE and\
                   board.spaces[self.posX][self.posY + 1] != COBRA2_SPACE:
                    # If the opponent would turn back on itself, it needs to move left or right before going down.
                    if self.direction == "Up":
                        if self.posX > self.target.posX:
                            self.direction = "Left"
                        else:
                            self.direction = "Right"
                    else:
                        self.direction = "Down"        
                # If there is an obstacle, look for an empty spot to move to.
                else:
                    if board.spaces[self.posX - 1][self.posY] == EMPTY_SPACE\
                    and self.posX > self.target.posX:
                        self.direction = "Left"
                    elif board.spaces[self.posX + 1][self.posY] == EMPTY_SPACE\
                    and self.posX <= self.target.posX:
                        self.direction = "Right"
                    elif board.spaces[self.posX][self.posY - 1] == EMPTY_SPACE:
                        self.direction = "Up"

def check_collision(board, cobra):
    if (cobra.posX < 0) or (cobra.posY < 0) or (cobra.posX > BOARD_SIZE_WIDTH - 1)\
    or (cobra.posY > BOARD_SIZE_HEIGHT - 1) or (board.spaces[cobra.posX][cobra.posY] == COBRA1_SPACE)\
    or (board.spaces[cobra.posX][cobra.posY] == COBRA2_SPACE):
        collision = True
    else:
        collision = False

    return collision

def update_segments(board, cobra):
    posX = cobra.posX
    posY = cobra.posY

    if board.spaces[posX][posY] == FOOD_SPACE:
        for i in range(0, cobra.segmentsToAdd):
            cobra.add_segment(cobra.Segment(posX, posY))
        # Defaults to first piece of food for now.  May have more than once piece on board at a time in the future.
        del board.foodList[0]
        board.amountOfFood -= 1
        if board.amountOfFood == 0:
            board.foodOnBoard = False

    for seg in cobra.segments:
        prevPosX = seg.posX
        prevPosY = seg.posY
        board.spaces[prevPosX][prevPosY] = EMPTY_SPACE
        seg.posX = posX
        seg.posY = posY
        board.spaces[seg.posX][seg.posY] = cobra.spaceType
        posX = prevPosX
        posY = prevPosY

def main():
    # Set board size, cobra starting position, create first cobra segment, and initialize display
    board1 = Board(BOARD_SIZE_WIDTH, BOARD_SIZE_HEIGHT, BOARD_SPACE_SIZE)
    cobra1 = Cobra(PLAYER1_START_X, PLAYER1_START_Y, COBRA_START_DIRECTION, COBRA1_SPACE)
    cobra2 = Opponent(OPPONENT_START_X, OPPONENT_START_Y, COBRA_START_DIRECTION, COBRA2_SPACE)
    cobra1.add_segment(Cobra.Segment(cobra1.posX, cobra1.posY))
    if OPPONENT_ON == True:
        cobra2.add_segment(Opponent.Segment(cobra2.posX, cobra2.posY))

    pygame.init()

    screen = pygame.display.set_mode((DISPLAY_RESOLUTION_WIDTH, DISPLAY_RESOLUTION_HEIGHT))
    gameRunning = True
    paused = False

    while gameRunning == True:

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
               if event.key == pygame.K_w:
                   cobra2.direction = "Up"
               if event.key == pygame.K_s:
                   cobra2.direction = "Down"
               if event.key == pygame.K_a:
                   cobra2.direction = "Left"
               if event.key == pygame.K_d:
                   cobra2.direction = "Right"
               if event.key == pygame.K_ESCAPE:
                   pygame.quit()
               if event.key == pygame.K_SPACE:
                   if not paused:
                       paused = True
                   else:
                       paused = False

        if not paused:
            update_segments(board1, cobra1)
            if OPPONENT_ON == True:
                update_segments(board1, cobra2)
            board1.draw_board(screen)
            pygame.display.update()

            if not board1.foodOnBoard:
                board1.create_food()

            cobra1.move()
            cobra1.collision = check_collision(board1, cobra1)

            if OPPONENT_ON == True:
                cobra2.check_target(board1)
                if cobra2.target.index == -1 and board1.foodOnBoard == True:
                    if cobra2.turnsToWait == 0:
                        cobra2.get_food_target(board1)
                        cobra2.turnsToWait = OPPONENT_TURNS_TO_WAIT
                    else:
                        cobra2.turnsToWait -= 1
                cobra2.set_direction(board1)

                cobra2.move()
                cobra2.collision = check_collision(board1, cobra2)
                if cobra2.collision == True:
                    gameRunning = False

            cobra1.collision = check_collision(board1, cobra1)

            if cobra1.collision == True:
                gameRunning = False

            pygame.time.wait(MOVEMENT_DELAY)

main()