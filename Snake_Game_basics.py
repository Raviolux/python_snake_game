import pygame
from pygame.locals import *
import time


class Player(object):
    x = 10
    y = 10
    speed = 1
    direction = 0

    def update(self):
        if self.direction == 0:
            self.x += self.speed
        elif self.direction == 1:
            self.x -= self.speed
        elif self.direction == 2:
            self.y -= self.speed
        elif self.direction == 3:
            self.y += self.speed

    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3


class App(object):
    window_width = 800
    window_height = 600
    player = None

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.player = Player()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.HWSURFACE
        )

        pygame.display.set_caption('Hello world! Pygame example :D')
        self._running = True
        self._image_surf = pygame.image.load('pygame.png').convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            # time.sleep(1)
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
        self.on_cleanup()


if __name__ == '__main__':
    theApp = App()
    theApp.on_execute()
