import pygame
from pygame.locals import *
import time
from random import randint

"""Bugs found:
- Passed apple two different coordinates fomats in init and in body of code:
    in init passed 0,5 and apple did multiplication by step.
    in body passed 0,5 and apple DID NOT do multiplication.
    FIXED adding method NEW_POS to multiply always
    
- changed collsion box from 100 (=step) to 99 (=step-1) to be sure that when flanking target
    there would be no accidental collision.
    
- followed example in initialising lots of snake blocks to prevent spawn errors"""


class Apple(object):
    x = 0
    y = 0
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    step = 100

    def __init__(self, surface, x=0, y=0):
        self.game = surface
        self.set_boundary()
        if x == 0 and y == 0:
            self.random_pos()
        else:
            self.new_pos(x, y)

    def set_boundary(self, min_x=0, min_y=0, max_x=0, max_y=0):
        self.min_x = min_x
        self.min_y = min_y
        if max_x == 0:
            self.max_x = self.game.window_width
        else:
            self.max_x = max_x
        if max_y == 0:
            self.max_y = self.game.window_height
        else:
            self.max_y = max_y

    # standard spawn
    def new_pos(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    # different way of handling spawn. Here the apple does everything
    def random_pos(self):
        self.x = randint(self.min_x / self.step, (self.max_x / self.step) - 1) * self.step
        self.y = randint(self.min_y / self.step, (self.max_y / self.step) - 1) * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Player(object):
    x = []
    y = []
    step = 100
    direction = 0
    length = 4

    update_count_max = 2
    update_count = 0

    def __init__(self, length):
        self.length = length
        for i in range(600):  # initialize a lot of blocks to prevent errors
            self.x.append(-220)  # assign number outside of play area
            self.y.append(-220)
        self.x[0] = 0  # set head to position (0,0)
        self.y[0] = 0
        self.x[1] = -100  # set first three blocks after head to safe position (no risk of clipping)
        self.x[2] = -200
        self.x[3] = -300

    def update(self):
        self.update_count += 1
        if self.update_count > self.update_count_max:
            for i in range(self.length - 1, 0, -1):
                # print(f"self.x[{i}] = self.x[{i - 1}]  ---  self.y[{i}] = self.y[{i - 1}]")
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            if self.direction == 0:
                self.x[0] += self.step
            if self.direction == 1:
                self.x[0] -= self.step
            if self.direction == 2:
                self.y[0] -= self.step
            if self.direction == 3:
                self.y[0] += self.step

            self.update_count = 0

    def move_right(self):
        if self.direction == 1:
            pass
        else:
            self.direction = 0

    def move_left(self):
        if self.direction == 0:
            pass
        else:
            self.direction = 1

    def move_up(self):
        if self.direction == 3:
            pass
        else:
            self.direction = 2

    def move_down(self):
        if self.direction == 2:
            pass
        else:
            self.direction = 3

    def draw(self, surface, image):
        for i in range(self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class Game:

    def __init__(self):
        self.window_width = 800
        self.window_height = 600

    @staticmethod
    def is_collision(x1, y1, x2, y2, block_size):
        if x2 <= x1 <= x2 + block_size:
            if y2 <= y1 <= y2 + block_size:
                return True
        return False


class App(object):
    player = None
    apple = None

    def __init__(self, surface):
        self._running = True
        self._display_surf = None
        self._snake_block = None
        self._apple_block = None
        self.game = surface
        self.player = Player(4)
        self.apple = Apple(self.game, randint(0, 7), randint(0, 5))
        self.red = self.green = self.blue = 0
        print(self.apple.x, self.apple.y)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.game.window_width,
                                                      self.game.window_height),
                                                     pygame.HWSURFACE)
        pygame.display.set_caption('Pygame snake example gnagnagnagnagna batmaaan')
        self._running = True
        self._snake_block = pygame.image.load('snake.png').convert()
        self._apple_block = pygame.image.load('apple.png').convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        # collision check with apple
        if self.game.is_collision(self.apple.x, self.apple.y, self.player.x[0], self.player.y[0], 99):
            print('got apple!')
            self.apple.new_pos(randint(0, 7), randint(0, 5))
            print('new apple: ', self.apple.x, self.apple.y)  # there i'm printing the NEW position of the apple
            self.player.length += 1

        # collision check with snake
        for i in range(2, self.player.length):
            # range (2, length) because head cannot collide with itself or the two blocks behind it)
            if self.game.is_collision(self.player.x[0], self.player.y[0],
                                      self.player.x[i], self.player.y[i], 95):
                print('Collision! You lost.')
                exit(0)

        # collision check with walls
        if self.game.is_collision(self.player.x[0], self.player.y[0], 801, -201, 1000) or \
                self.game.is_collision(self.player.x[0], self.player.y[0], -201, 601, 1200) or \
                self.game.is_collision(self.player.x[0], self.player.y[0], -1001, -201, 1000) or \
                self.game.is_collision(self.player.x[0], self.player.y[0], -201, -1201, 1200):
            print('Collision! You lost.')
            exit(0)

    def on_render(self):
        if self.blue < 255:
            self.blue += 1
        elif self.green < 255:
            self.green += 1
        elif self.red < 255:
            self.red += 1
        else:
            self.green = self.red = self.blue = 0
        self._display_surf.fill((self.red, self.green, self.blue))
        self.player.draw(self._display_surf, self._snake_block)
        self.apple.draw(self._display_surf, self._apple_block)
        pygame.display.flip()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:  # come cazzo fa questa riga a lanciare ON_INIT() cazzo??
            # perche le () indicano una chiamata
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.player.move_right()
            if keys[K_LEFT]:
                self.player.move_left()
            if keys[K_UP]:
                self.player.move_up()
            if keys[K_DOWN]:
                self.player.move_down()

            if keys[K_ESCAPE]:
                self._running = False
            self.on_loop()
            self.on_render()

            time.sleep(0.1)
        self.on_cleanup()


if __name__ == '__main__':
    the_surface = Game()
    the_app = App(the_surface)
    the_app.on_execute()
