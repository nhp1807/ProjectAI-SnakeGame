import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('font/arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (85, 110, 240)
BLUE2 = (0, 100, 255)
GREEN1 = (111,178,80)
GREEN2 = (134,209,96)
GREEN_SNAKE = (115,182,113)
GREEN_SNAKE_2 = (106,158,104)
GREEN_SNAKE_HEAD = (180,58,57)
BLACK = (0, 0, 0)
YELLOW_BG = (247,230,151)
YELLOW_BG_2 = (188,177,130)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        # Create the snake
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        # Create barrier
        self.barrier = [Point(80, 360), Point(80, 340)]
        i = 1
        j = 220
        k = 400
        while i <= 3:
            self.barrier.append(Point(200, (i+5)*20))
            self.barrier.append(Point(40, i*20))
            self.barrier.append(Point(600, (i+17)*20))
            self.barrier.append(Point(k, 200))
            self.barrier.append(Point(j, 340))
            k += 20
            j += 20
            i += 1

        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake or self.food in self.barrier:
            self._place_food()
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        # hits the barrier
        if self.head in self.barrier[0:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(YELLOW_BG)
        x = 0
        y = 0
        while True:
            pygame.draw.rect(self.display, YELLOW_BG_2, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
            x += 40
            if (x>620):
                if((y//BLOCK_SIZE) % 2 == 0):
                    x = 20
                    y += 20
                    pygame.draw.rect(self.display, YELLOW_BG_2, pygame.Rect(
                        x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif((y//BLOCK_SIZE) % 2 == 1):
                    x = 0
                    y += 20
                    pygame.draw.rect(self.display, YELLOW_BG_2, pygame.Rect(
                        x, y, BLOCK_SIZE, BLOCK_SIZE))
                if(y > 460):
                    break
        
        # Fill the snake
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN_SNAKE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN_SNAKE_2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        for pt in self.barrier:
            pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLACK, pygame.Rect(
                self.snake[0].x, self.snake[0].y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.circle(self.display, GREEN_SNAKE_HEAD, (self.snake[0].x +10, self.snake[0].y +10), BLOCK_SIZE/1.5)

        # Fill the food
        # pygame.draw.rect(self.display, RED, pygame.Rect(
        #     self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        food_image = pygame.image.load("image/coin.png").convert()
        
        # Fill the barrier
        barrier_image = pygame.image.load("image/brick.png").convert()

        # Display the score    
        text = font.render("Score: " + str(self.score), True, BLACK)
        self.display.blit(text, [0, 0])
        self.display.blit(food_image, (self.food.x, self.food.y))

        # Display the barrier
        self.display.blit(barrier_image, [80, 360])
        self.display.blit(barrier_image, [80, 340])
        i = 1
        j = 220
        k = 400
        while i <= 3:
            self.display.blit(barrier_image, Point(200, (i+5)*20))
            self.display.blit(barrier_image, Point(40, i*20))
            self.display.blit(barrier_image, Point(600, (i+17)*20))
            self.display.blit(barrier_image, Point(k, 200))
            self.display.blit(barrier_image, Point(j, 340))
            k += 20
            j += 20
            i += 1

        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)

    def start_game():
        game = SnakeGame()
    
        # game loop
        while True:
            game_over, score = game.play_step()
        
            if game_over == True:
                print('Final Score', score)
                # break
                game = SnakeGame()

if __name__ == '__main__':
    SnakeGame.start_game()
    pygame.quit()