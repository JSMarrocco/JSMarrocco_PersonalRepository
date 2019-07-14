from bird import Bird
from pipes import PipesPairs
from wall import Wall
from networkGraph import NetworkGraph

import pygame, sys, random, time

sys.path.insert(0, './neat_algorithm')
from genomes import Genomes
from deepNeuralNetwork import DeepNeuralNetwork, ActivationFunctions

COLOR_SKY = (51, 204, 255)
COLOR_YELLOW = (255, 255, 102)
COLOR_GREY = (77, 77, 77)
COLOR_WHITE = (192, 192, 192)


class Game:

    def __init__(self, settings):
        self.settings = settings
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(settings['SCREEN_RECT'].size, winstyle, 32)
        self.screen = pygame.display.set_mode(settings['SCREEN_RECT'].size, winstyle, bestdepth)

        self.gameOver = False

        self.genomes_poll = Genomes(3, 2, settings['POPULATION_SIZE'], settings)
        self.birds = []
        for i in range(settings['POPULATION_SIZE']):
            self.birds.append(Bird(100, 220, getRandomColor(),
                                   DeepNeuralNetwork(ActivationFunctions.RELU, ActivationFunctions.SOFTMAX, self.genomes_poll.genomes[i])))
        self.best_bird = self.birds[0]

        self.pipePairs = PipesPairs()
        self.floor = Wall(0, settings['SCREEN_RECT'].height - 10, settings['SCREEN_RECT'].width, 25, COLOR_GREY)
        self.ceiling = Wall(0, - 10, settings['SCREEN_RECT'].width, 10, COLOR_GREY)
        self.right_wall = Wall(480, 0, 15, settings['SCREEN_RECT'].height, COLOR_GREY)
        self.blue_wall = Wall(480, 0, settings['SCREEN_RECT'].width - 480, settings['SCREEN_RECT'].height, COLOR_SKY)

        self.graph = NetworkGraph()

        self.objects = [self.pipePairs, self.floor, self.blue_wall, self.right_wall, self.graph]

        self.generation = 1
        self.high_score = 0
        self.nb_bird_alive = settings['POPULATION_SIZE']

    def handle_game(self):
        while True:

            clock = pygame.time.Clock()

            while self.isPopulationAlive():
                self.handle_events()
                self.handle_collision()
                self.update()
                self.draw()
                pygame.display.update()
                clock.tick(60)

            time.sleep(1)

            self.__update_data()
            self.__evolve_population()

            self.pipePairs = PipesPairs()
            self.best_bird = None
            self.objects = [self.pipePairs, self.floor, self.blue_wall, self.right_wall, self.graph]

    def __evolve_population(self):
        self.genomes_poll.genomes = []
        for bird in self.birds:
            self.genomes_poll.genomes.append(bird.brain.genome)
        self.genomes_poll.evolve()
        self.birds = []
        for i in range(self.settings['POPULATION_SIZE']):
            self.birds.append(Bird(100, 220, getRandomColor(),
                                   DeepNeuralNetwork(ActivationFunctions.RELU, ActivationFunctions.SOFTMAX,
                                                     self.genomes_poll.genomes[i])))

    def draw(self):
        self.screen.fill(COLOR_SKY)
        for bird in self.birds:
            bird.draw(self.screen)
        for o in self.objects:
            o.draw(self.screen)

        self.__draw_data()

    def update(self):
        next_pipe_x, top_pipe_y, bottom_pipe_y = self.pipePairs.getNextPtrBounds()
        for bird in self.birds:
            if bird.drawable:
                bird.update([next_pipe_x - bird.bounds.x, top_pipe_y - bird.bounds.y, bottom_pipe_y - bird.bounds.y])
        self.pipePairs.update()

    def handle_collision(self):
        for bird in self.birds:
            if bird.isAlive:
                if bird.bounds.colliderect(self.floor.bounds) or bird.bounds.colliderect(self.ceiling.bounds):
                    bird.isAlive = False
                for pair in self.pipePairs.pairs:
                    for pipe in pair.pipes:
                        if bird.bounds.colliderect(pipe.bounds):
                            bird.isAlive = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

    def isPopulationAlive(self):
        for bird in self.birds:
            if bird.isAlive:
                return True

        return False

    def __draw_data(self):
        tmp_best_bird = sorted(self.birds, key=lambda x: x.brain.genome.fitness, reverse=True)[0]
        if tmp_best_bird is not self.best_bird:
            self.best_bird = tmp_best_bird
            self.graph.set_graph(self.best_bird.brain.genome)

        self.screen.blit(pygame.font.SysFont("arial", 32).render("Gen: " + str(self.generation), 1, COLOR_GREY),
                         (510, 0))
        self.screen.blit(pygame.font.SysFont("arial", 32).render("Highest score: " + str(self.high_score), 1, COLOR_GREY),
                         (510, 42))
        if self.generation > 1:
            settings = self.genomes_poll.settings
        else:
            settings = self.settings
        self.screen.blit(pygame.font.SysFont("arial", 32).render("Crossover odds: " + str(int(settings['CROSSOVER_ODDS'] * 100)) + '%', 1, COLOR_GREY),
                         (510, 84))
        self.screen.blit(pygame.font.SysFont("arial", 32).render("Mutation odds: " + str(int((1 - settings['CROSSOVER_ODDS']) * settings['MUTATION_ODDS'] * 100)) + '%', 1, COLOR_GREY),
                         (510, 126))

        self.screen.blit(pygame.font.SysFont("arial", 32).render("Score: " + str(self.best_bird.score), 1, COLOR_GREY),
                         (800, 00))

        self.screen.blit(pygame.font.SysFont("arial", 32).render("Population:" + str(len([x for x in self.birds if x.isAlive])), 1, COLOR_GREY),
                         (800, 42))

    def __update_data(self):
        self.generation += 1
        new_score = sorted(self.birds, key=lambda x: x.score, reverse=True)[0].score
        if self.best_bird.score > self.high_score:
            self.high_score = new_score

        self.nb_bird_alive = self.settings['POPULATION_SIZE']


def getRandomColor():
    return random.randint(50, 205), random.randint(50, 205), random.randint(50, 205)
