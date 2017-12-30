import pygame
from pygame.locals import *

PIXELS_PER_GRID = 20

class Snake:
    def __init__(self, game, startingCoordinate, startingDirection):
        self.game = game

        self.chain = [startingCoordinate]
        for i in range(10):
            n = [startingCoordinate[0]-i-1, startingCoordinate[1]]
            self.chain.append(n)

        self.direction = startingDirection
        self.speed = 150

        self.speedtimer = 0

    def on_loop(self, deltaTicks):
        self.speedtimer += deltaTicks
        if self.speedtimer > self.speed:
            self.speedtimer = 0
            self.update()

    def update(self):

        # Move snake body

        for i in reversed(range(len(self.chain))):
            if i!= 0:
                self.chain[i][0] = self.chain[i-1][0]
                self.chain[i][1] = self.chain[i-1][1]

        # Move snake head

        if self.direction == 0:
            self.chain[0][0] += 1
        if self.direction == 1:
            self.chain[0][1] += 1
        if self.direction == 2:
            self.chain[0][0] += -1
        if self.direction == 3:
            self.chain[0][1] += -1

        # Check head in wall

        if self.chain[0][0] >= self.game.gridSize[0]:
            self.kill()
        if self.chain[0][1] >= self.game.gridSize[1]:
            self.kill()
        if self.chain[0][0] < 0:
            self.kill()
        if self.chain[0][1] < 0:
            self.kill()

        # Check head in other snake's body

        collided = self.game.snakeCollision(self)

        if type(collided) == Snake:
            self.kill(collided)

    def on_render(self, screen):
        for i in range(len(self.chain)):
            rect = (self.chain[i][0] * PIXELS_PER_GRID, self.chain[i][1] * PIXELS_PER_GRID, PIXELS_PER_GRID, PIXELS_PER_GRID)
            if i == 0:
                pygame.draw.rect(screen, [100, 100, 100], rect, 0)
            else:
                pygame.draw.rect(screen, [75, 75, 75], rect, 0)

    def setDirection(self, direction):
        if (self.direction - direction)%2 != 0:
            self.direction = direction

    def kill(self, killedBy = None):
        if killedBy == self:
            print("I SUICIDED")
        elif killedBy == None:
            print("Killed by the world")
        else:
            print("I HAVE BEEN MURDERED")


class Game:
    def __init__(self, gridSize):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = PIXELS_PER_GRID*gridSize[0], PIXELS_PER_GRID*gridSize[1]
        self.gridSize = gridSize

        self.ticksPassed = 0
        self.deltaTicks = 0

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self.ownSnake = Snake(self, [10,0], 0)
        self.otherSnakes = [Snake(self, [5,2], 0)]

    def snakeCollision(self, snake):
        coordinate = snake.chain[0]

        # Check if collision with ownSnake

        for i in range(len(self.ownSnake.chain)):
            if i != 0 or snake != self.ownSnake:
                if self.ownSnake.chain[i][0] == coordinate[0] and self.ownSnake.chain[i][1] == coordinate[1]:
                    return self.ownSnake

        # Check collision with one of the other snakes

        for otherSnake in self.otherSnakes:
            for i in range(len(otherSnake.chain)):
                if i != 0 or snake != otherSnake:
                    if otherSnake.chain[i][0] == coordinate[0] and otherSnake.chain[i][1] == coordinate[1]:
                        return otherSnake

        return False

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


            if event.key == pygame.K_j:
                self.otherSnakes[0].setDirection(2)
            if event.key == pygame.K_i:
                self.otherSnakes[0].setDirection(3)
            if event.key == pygame.K_l:
                self.otherSnakes[0].setDirection(0)
            if event.key == pygame.K_k:
                self.otherSnakes[0].setDirection(1)


    def on_loop(self):
        self.deltaTicks = pygame.time.get_ticks() - self.ticksPassed
        self.ticksPassed = pygame.time.get_ticks()

        self.ownSnake.on_loop(self.deltaTicks)

        for i in self.otherSnakes:
            i.on_loop(self.deltaTicks)

    def on_render(self):
        self._display_surf.fill([0, 0, 0])

        self.ownSnake.on_render(self._display_surf)
        for i in self.otherSnakes:
            i.on_render(self._display_surf)

        pygame.display.flip()

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
