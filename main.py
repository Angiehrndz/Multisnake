import pygame
from pygame.locals import *

class Snake:
    def __init__(self, startingCoordinate, startingDirection):
        self.chain = [startingCoordinate]
        self.direction = startingDirection

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def setDirection(self, direction):
        if (self.direction - direction) %2 != 0:
            self.direction = direction
        print(str(direction) + " " +str(self.direction))


class Game:
    def __init__(self, gridSize):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 20*gridSize[0], 20*gridSize[1]
        self.gridSize = gridSize

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self.ownSnake = Snake([0,0], 0)
        self.otherSnakes = []

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.ownSnake.setDirection(2)
            if event.key == pygame.K_w:
                self.ownSnake.setDirection(3)
            if event.key == pygame.K_d:
                self.ownSnake.setDirection(0)
            if event.key == pygame.K_s:
                self.ownSnake.setDirection(1)

    def on_loop(self):
        self.ownSnake.on_loop()

        for i in self.otherSnakes:
            i.on_loop()

    def on_render(self):
        self.ownSnake.on_render()

        for i in self.otherSnakes:
            i.on_render()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()



if __name__ == "__main__":
    game = Game([60, 40])
    game.on_execute()
