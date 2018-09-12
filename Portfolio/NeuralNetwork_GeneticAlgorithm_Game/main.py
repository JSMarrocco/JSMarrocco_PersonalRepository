import pygame, time, sys
from collections import defaultdict
from gameObject import GameObject
from player import Player, Population
from geneticAlgorithm import evolve

# CONST
SCREENRECT = pygame.Rect(0, 0, 640, 580)
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (192, 192, 192)
COLOR_GOLDEN = (216, 179, 0)
PLAYER_VELOCITY = 3

settings = defaultdict()
settings['GAME_TIME_LIMIT'] = 6
settings['POPULATION_SIZE'] = 25
settings['ELITISM'] = 0.12
settings['REPRODUCE_ODDS'] = 0.8
settings['CROSSOVER_ODDS'] = 0.4
settings['MUTATION_ODDS'] = 0.05

class Wall(GameObject):
    def __init__(self, x, y, w, h, color, special_effect=None):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.special_effect = special_effect

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)


class Nugget(GameObject):
    def __init__(self, x, y, w, h, color, special_effect=None):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.special_effect = special_effect

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

class Game:
    def __init__(self):
        self.objets = []
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.walls = []
        self.gameWon = False
        self.gameOver = False
        self.gen = 1
        self.score = 1000

        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        self.screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

        self.nugget = Nugget(SCREENRECT.centerx, 50, 5, 5, COLOR_GOLDEN)
        self.walls.append(Wall(0, 0, 10, 480, COLOR_WHITE))
        self.walls.append(Wall(SCREENRECT.width - 10, 0, 10, 480, COLOR_WHITE))
        self.walls.append(Wall(0, 0, SCREENRECT.width, 10, COLOR_WHITE))
        self.walls.append(Wall(0, 480 - 10, SCREENRECT.width, 10, COLOR_WHITE))
        self.walls.append(Wall(SCREENRECT.centerx - 50, SCREENRECT.centery - 5, 100, 10, COLOR_WHITE))
        self.walls.append(Wall(SCREENRECT.centerx + 100, SCREENRECT.centery - 100, 100, 10, COLOR_WHITE))
        self.walls.append(Wall(SCREENRECT.centerx - 200, SCREENRECT.centery - 100, 100, 10, COLOR_WHITE))

        self.population = Population(settings['POPULATION_SIZE'], self.nugget, self.walls)

        self.player = Player(SCREENRECT.centerx, 430, 5, 5, (0, 218, 204), self.nugget, self.walls, None,True)

        for wall in self.walls:
            self.objets.append(wall)
        self.objets.append(self.nugget)
        self.objets.append(self.player)

    def draw(self):
        self.screen.fill(COLOR_BLACK)
        for o in self.objets:
            o.draw(self.screen)
        self.screen.blit(self.scoreLabel, (50, 530))
        self.screen.blit(self.genLabel, (300, 530))
        self.population.draw(self.screen)

    def update(self):
        for o in self.objets:
            o.update()

        myfont = pygame.font.SysFont("monospace", 32)
        self.scoreLabel = myfont.render("Score: " + str(int(self.score)), 1, COLOR_WHITE)
        self.genLabel = myfont.render("Generation: " + str(self.gen), 1, COLOR_WHITE)

        self.population.update()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                return
        if (self.player.isAlive):
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.player.move_right()
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.player.move_left()
            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.player.move_up()
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.player.move_down()

    def handle_collisions(self):
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

        # Hit a walls
        for wall in self.walls:
            edge = intersect(wall, self.player)
            if edge is None:
                continue
            if edge == 'left':
                self.player.move_left()
            elif edge == 'right':
                self.player.move_right()
            elif edge == 'top':
                self.player.move_up()
            elif edge == 'bottom':
                self.player.move_down()

            self.player.kill()

        # Hit nugget
        if intersect(self.nugget, self.player):
            self.gameWon = True

        self.population.handle_collision()

def timeOut():
    print('time out')

def main():
    # Init PyGame
    pygame.init()
    window = pygame.display.set_mode((600, 300))

    # Set the display mode
    # gameLoop()
    game = Game()
    clock = pygame.time.Clock()

    while True:
        start = time.time()
        while True:
            game.handle_events()
            game.handle_collisions()
            game.update()
            game.draw()
            if game.population.isExtinct() or time.time() - start >= settings['GAME_TIME_LIMIT']: break
            pygame.display.update()
            clock.tick(90)
        if game.gameWon: break
        game.population.players, game.gen, game.score =  evolve(settings, game.population.players, game.gen, game.score)

    time.sleep(1)
    pygame.quit()


#call the "main" function if running this script
if __name__ == '__main__': main()