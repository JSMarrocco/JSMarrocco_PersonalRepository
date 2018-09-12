from gameObject import GameObject
import pygame, math
from random import randint
from neuralnetwork import NeuralNetwork

PLAYER_VELOCITY = 1
SCREENRECT = pygame.Rect(0, 0, 640, 580)

class Player(GameObject):
    def __init__(self, x, y, w, h, color, goal, obstacles=[], brain=None, special_effect=None):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.fitness = 1000
        self.isAlive = True
        self.obstacles = obstacles
        self.obstaclesAwareness = []
        self.goal = goal
        self.brain = NeuralNetwork([len(self.obstacles) * 3 + 1, len(self.obstacles) * 3 + 1, 2]) if brain is None else brain
        self.specialEffect = special_effect

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def move_right(self):
        self.move(PLAYER_VELOCITY, 0)

    def move_left(self):
        self.move(-PLAYER_VELOCITY, 0)

    def move_down(self):
        self.move(0, PLAYER_VELOCITY)

    def move_up(self):
        self.move(0, -PLAYER_VELOCITY)

    def kill(self):
        self.isAlive = False;

    def update(self):
        '''
            Update the fitness value and update position with the prediction made by the neural network
        '''
        if self.isAlive:
            if self.specialEffect is not True:
                tmpFitness = getDistanceBetween(self, self.goal)
                if tmpFitness < self.fitness: self.fitness = tmpFitness
                self.updateObstaclesAwareness()
                self.speed = self.transalteBrainPrediction()
                self.move(*self.speed)

    def updateObstaclesAwareness(self):
        '''
        :return: distance between every obstacle ( distance = sqrt( (|x1 - x2|)^2 *  (|y1 - y2|)^2 ) )
        '''
        self.obstaclesAwareness = []
        for o in self.obstacles:
            self.obstaclesAwareness.append(math.sqrt(pow(abs(self.centerx - o.centerx), 2) + pow(abs(self.centery - o.centery), 2)))
            self.obstaclesAwareness.append(math.sqrt(pow(abs(self.centerx - o.bounds.x), 2) + pow(abs(self.centery - o.bounds.y), 2)))
            self.obstaclesAwareness.append(math.sqrt(pow(abs(self.centerx - o.bounds.x - o.bounds.w), 2) + pow(abs(self.centery - o.bounds.y - o.bounds.h), 2)))

        return self.obstaclesAwareness

    def handle_collision(self):
        '''
            Check if the player intersect with a obstacle or the goal
        '''
        def intersect(obj, wall):
            edges = dict(
                left= pygame.Rect(obj.left, obj.top, 1, obj.height),
                right= pygame.Rect(obj.right, obj.top, 1, obj.height),
                top= pygame.Rect(obj.left, obj.top, obj.width, 1),
                bottom= pygame.Rect(obj.left, obj.bottom, obj.width, 1))
            collisions = set(edge for edge, rect in edges.items() if
                             wall.bounds.colliderect(rect))

            if not collisions:
                return None

            if len(collisions) == 1:
                return list(collisions)[0]

            if 'top' in collisions:
                if wall.centery >= obj.top:
                    return 'top'
                if wall.centerx < obj.left:
                    return 'left'
                else:
                    return 'right'

            if 'bottom' in collisions:
                if wall.centery >= obj.bottom:
                    return 'bottom'
                if wall.centerx < obj.left:
                    return 'left'
                else:
                    return 'right'

        for wall in self.obstacles:
            edge = intersect(wall, self)
            if edge is None:
                continue
            if edge == 'left':
                self.move_left()
            elif edge == 'right':
                self.move_right()
            elif edge == 'top':
                self.move_up()
            elif edge == 'bottom':
                self.move_down()

            self.kill()

        # Hit nugget
        if intersect(self.goal, self):
            self.fitness = 0
            self.kill()

    def transalteBrainPrediction(self):
        '''
            Use the neural network to predict the next move and translate the output
            so that the player can choose a move
        :return: array with velocity in x and y
        '''
        predict = self.brain.predict(self.obstaclesAwareness)
        if predict[0] <= 0.333:
            velocityH = PLAYER_VELOCITY

        elif  predict[0] > 0.333 and predict[0] <= 0.666:
            velocityH = -PLAYER_VELOCITY
        else:
            velocityH = 0

        if predict[1] <= 0.333:
            velocityV = PLAYER_VELOCITY

        elif predict[1] > 0.333 and predict[1] <= 0.666:
            velocityV = -PLAYER_VELOCITY
        else:
            velocityV = 0
        return [velocityH, velocityV]

class Population:
    def __init__(self, size, goal, obstacles):
        self.players = []
        for i in range(0, size):
            self.players.append(Player(
                SCREENRECT.centerx,
                430,
                5,
                5,
                (randint(50, 200), randint(50, 200), randint(50, 200)),
                goal,
                obstacles))

    def draw(self, surface):
        for p in self.players:
            p.draw(surface)

    def update(self):
        for p in self.players:
            p.update()

    def handle_collision(self):
        for p in self.players:
            p.handle_collision()

    def isExtinct(self):
        for p in self.players:
            if p.isAlive: return False

        return True




def getDistanceBetween(a ,b):
    if a is not None and b is not None:
        return math.sqrt(pow(abs(a.centerx - b.centerx), 2) + pow(abs(a.centery - b.centery), 2))
    return 0