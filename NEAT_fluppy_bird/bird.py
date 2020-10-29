from gameObject import GameObject
import pygame, time

FALL_VELOCITY = (0, 3.9)
NULL_VELOCITY = (0, 0)
FLAPPING_VELOCITY = (0, -4.5)
FLAPPING_MAX_TIME = 0.15
BIRD_RADIUS = 15
WINDOW_WIDTH = 480

COLOR_RED = (255, 0, 0)


class Bird(GameObject):
    def __init__(self, x, y, color, brain):
        GameObject.__init__(self, x, y, BIRD_RADIUS, BIRD_RADIUS, FALL_VELOCITY)
        self.color = color
        self.isFlapping = False
        self.flappingTime = 0
        self.brain = brain
        self.isAlive = True
        self.score = 0
        self.drawable = True

    def draw(self, surface):
        if self.drawable:
            pygame.draw.circle(surface, self.color, (self.bounds.x, self.bounds.y), self.bounds.height, self.bounds.width)

    def update(self, inputs):
        inputs[1] -= BIRD_RADIUS
        inputs[2] += BIRD_RADIUS
        if not self.isAlive:
            self.color = COLOR_RED
            if self.bounds.y < WINDOW_WIDTH - 10:
                self.speed = FALL_VELOCITY
            else:
                self.drawable = False
                self.speed = NULL_VELOCITY
        else:
            if self.isFlapping and time.time() - self.flappingTime >= FLAPPING_MAX_TIME:
                self.speed = FALL_VELOCITY
                self.isFlapping = False
            else:
                prediction = self.brain.feed_forward(inputs)
                if len(prediction) == 1 or (len(prediction) > 1 and prediction[0] < prediction[1]):
                    self.flap()

                if inputs[1] < 0 < inputs[2]:
                    self.brain.increment_fitness(1)

            if 0 >= inputs[0] > -2 and inputs[1] < 0 < inputs[2]:
                self.brain.increment_fitness(100)
                self.score += 1

        self.move(*self.speed)

    def flap(self):
        if not self.isFlapping:
            self.flappingTime = time.time()
            self.speed = FLAPPING_VELOCITY
            self.isFlapping = True

