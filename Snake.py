from enum import Enum
import random

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Snake:
    def __init__(self, speed=10):
        self.cells = []
        self.speed = speed
        self.size = 10
        self.direction = Direction.RIGHT
        self.head = None
        self.body = [
            [70, 50],
            [80, 50],
            [90, 50],
            [100, 50]
        ]
        self.screen = None
        self.clock = None
        self.has_fruit = False
        self.fruit = None
        self.fruit_position = []
        self.board = None

    def update_position(self, has_eaten: bool):
        snake_body = self.body[::-1]  # The snake with reversed order list
        last_pos = snake_body[0]  # The last positioned added aka the head

        if self.direction == Direction.RIGHT:
            self.body.append([last_pos[0] + self.size, last_pos[1]])
            if not has_eaten:
                del self.body[0]

        elif self.direction == Direction.LEFT:
            self.body.append([last_pos[0] - self.size, last_pos[1]])
            if not has_eaten:
                del self.body[0]

        elif self.direction == Direction.UP:
            self.body.append([last_pos[0], last_pos[1] - self.size])
            if not has_eaten:
                del self.body[0]

        elif self.direction == Direction.DOWN:
            self.body.append([last_pos[0], last_pos[1] + self.size])
            if not has_eaten:
                del self.body[0]

    def spawn_fruit(self):
        fruit_x = round(random.randrange(0, 500) / 10.0) * 10.0
        fruit_y = round(random.randrange(0, 500) / 10.0) * 10.0
        self.fruit_position = [fruit_x, fruit_y]

    def draw_fruit(self):
        fruit_x, fruit_y = self.fruit_position
        self.fruit = pygame.draw.rect(self.screen, RED, (fruit_x, fruit_y, self.size, self.size))
        self.has_fruit = True

    def fruit_collision(self):
        if self.fruit.colliderect(self.head):
            self.has_fruit = False
            return True
        return False

    def body_collision(self):
        for block in self.cells:
            if self.head.colliderect(block):
                return True
        return False

    def edge_collision(self):
        if self.board.contains(self.head):
            return False
        return True

    def is_game_over(self):
        if self.edge_collision():
            return True
        elif self.body_collision():
            return True
        return False

    def draw_snake(self):
        cells = []  # Local list used to store cell variables
        for block in self.body:
            (x, y, width, height) = (block[0], block[1], self.size, self.size)
            border_width = 1  # The border width of each cell of the snake
            cells.append(pygame.draw.rect(self.screen, GREEN, (x, y, width, height)))  # Draws and append each cell
            pygame.draw.rect(self.screen, BLACK, (x, y, width, height),
                             width=border_width)  # Draws the border of the cell
        self.head = cells.pop()  # Removes the last cell aka the head of the snake
        self.cells = cells  # Updates the body cells

    def draw_game(self):
        self.screen.fill(BLACK)  # Sets the background color
        self.board = pygame.draw.rect(self.screen, BLACK,
                                      (0, 0, 500, 500))  # Draws the board rect to check for out-of-map collision.
        self.draw_fruit()  # Draws the fruit
        self.draw_snake()  # Draws the snake

    def game_loop(self):
        if not self.has_fruit:
            self.spawn_fruit()
        self.draw_game()
        has_eaten = self.fruit_collision()
        self.update_position(has_eaten)
        self.clock.tick(self.speed)
        pygame.display.update()
        return self.is_game_over()

    def run(self):
        self.create_window()
        running = True
        while running:
            game_over = self.game_loop()
            if game_over:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_LEFT:
                        if self.direction != Direction.RIGHT:
                            self.direction = Direction.LEFT
                    if event.key == pygame.K_RIGHT:
                        if self.direction != Direction.LEFT:
                            self.direction = Direction.RIGHT
                    if event.key == pygame.K_UP:
                        if self.direction != Direction.DOWN:
                            self.direction = Direction.UP
                    if event.key == pygame.K_DOWN:
                        if self.direction != Direction.UP:
                            self.direction = Direction.DOWN

        pygame.quit()

    def create_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
