from gameObject import GameObject

import pygame, random

COLOR_GREEN = (0, 204, 0)
PIPE_WIDTH = 43
PIPE_HEIGHT_MIN = 100
PIPE_HEIGHT_MAX = 340
GAP_BETWEEN_PAIRS = PIPE_WIDTH * 4
GAP_SIZE = 110
WINDOW_WIDTH = 480
PIPE_VELOCITY = (-2, 0)


class Pipe(GameObject):
    def __init__(self, x, y, w, h, color):
        GameObject.__init__(self, x, y, w, h, PIPE_VELOCITY)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)


class PipesPair:
    def __init__(self, x):
        self.pipes = [Pipe(x, 0, PIPE_WIDTH, random.randint(PIPE_HEIGHT_MIN, PIPE_HEIGHT_MAX), COLOR_GREEN)]
        tmp_size = self.pipes[0].height + GAP_SIZE
        self.pipes.append(Pipe(x, tmp_size, PIPE_WIDTH, WINDOW_WIDTH - tmp_size, COLOR_GREEN))

    def draw(self, surface):
        for pipe in self.pipes:
            pipe.draw(surface)

    def update(self):
        for pipe in self.pipes:
            pipe.update()

    def getPairsBounds(self):
        return self.pipes[0].bounds


class PipesPairs:
    def __init__(self):
        self.pairs = [PipesPair(WINDOW_WIDTH / 2 + PIPE_WIDTH)]
        self.nextPtr = self.pairs[0]
        for i in range(1, 3):
            self.pairs.append(PipesPair(self.pairs[i - 1].getPairsBounds().x + GAP_BETWEEN_PAIRS))

    def draw(self, surface):
        for pair in self.pairs:
            pair.draw(surface)

    def update(self):
        for pair in self.pairs:
            pair.update()

        self.updatePairsList()
        self.updateNextPtr()

    def updateNextPtr(self):
        if self.nextPtr.getPairsBounds().centerx < 100:
            self.nextPtr = self.pairs[self.pairs.index(self.nextPtr) + 1]

    def updatePairsList(self):
        if self.pairs[0].getPairsBounds().x <= -PIPE_WIDTH:
            self.pairs.pop(0)
            self.pairs.append(PipesPair(self.pairs[len(self.pairs) - 1].getPairsBounds().x + GAP_BETWEEN_PAIRS))

    def getNextPtrBounds(self):
        return self.nextPtr.getPairsBounds().centerx, self.nextPtr.pipes[0].bounds.y + self.nextPtr.pipes[0].height, self.nextPtr.pipes[1].bounds.y
