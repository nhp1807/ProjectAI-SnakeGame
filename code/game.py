import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('font/arial.ttf', 25)


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
SPEED = 50


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        import agent
        # text = font.render("Record: " + str(agent.record), True, BLACK)
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        # create a snake with 3 blocks
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        # Create barrier
        self.barrier = [Point(80, 360), Point(80, 340)]
        i = 1
        j = 220
        k = 400
        # while i <= 2:
        self.barrier.append(Point(200, (i+5)*20))
        self.barrier.append(Point(40, i*20))
        self.barrier.append(Point(600, (i+17)*20))
        self.barrier.append(Point(k, 200))
        self.barrier.append(Point(j, 340))
            # k += 20
            # j += 20
            # i += 1
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake or self.food in self.barrier:
            self._place_food()
        for pt in self.barrier:
            if self.food.x == pt.x or self.food.y == pt.y:
                self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        # hits the barrier
        if self.head in self.barrier[0:]:
            return True

        return False

    def _update_ui(self):
        # Fill the background
        self.display.fill(YELLOW_BG)
        x = 0
        y = 0
        while True:
            pygame.draw.rect(self.display, YELLOW_BG_2, pygame.Rect(
                x, y, BLOCK_SIZE, BLOCK_SIZE))
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
            pygame.draw.rect(self.display, GREEN_SNAKE, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN_SNAKE_2,
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        
        pygame.draw.circle(self.display, GREEN_SNAKE_HEAD, (self.snake[0].x +10, self.snake[0].y +10), BLOCK_SIZE/1.5)
        
        # Fill the food
        # pygame.draw.rect(self.display, RED, pygame.Rect(
        #     self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        food_image = pygame.image.load("image/coin.png").convert()
        
        # Fill the barrier
        barrier_image = pygame.image.load("image/brick.png").convert()

        # Display the score
        text = font.render("Score: " + str(self.score), True, BLACK)
        
        self.display.blit(food_image, (self.food.x, self.food.y))
        self.display.blit(text, (0, 0))
        
        # Display the barrier
        self.display.blit(barrier_image, [80, 360])
        self.display.blit(barrier_image, [80, 340])
        i = 1
        j = 220
        k = 400
        # while i <= 2:
        self.display.blit(barrier_image, Point(200, (i+5)*20))
        self.display.blit(barrier_image, Point(40, i*20))
        self.display.blit(barrier_image, Point(600, (i+17)*20))
        self.display.blit(barrier_image, Point(k, 200))
        self.display.blit(barrier_image, Point(j, 340))
            # k += 20
            # j += 20
            # i += 1

        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN,
                      Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
