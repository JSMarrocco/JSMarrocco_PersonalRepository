from collections import defaultdict

import pygame
import time

from game import Game

settings = defaultdict()
settings['SCREEN_RECT'] = pygame.Rect(0, 0, 980, 480)
settings['GAME_TIME_LIMIT'] = 6
settings['POPULATION_SIZE'] = 25
settings['ELITISM'] = 0.67                  # Percentage of elites in a specie (The ones that will be allow to reproduce)
settings['CROSSOVER_ODDS'] = 0.6            # Odds of genomes reproducing with another one
settings['MUTATION_ODDS'] = 1               # Odds of genomes mutating if not reproducing with another one
settings['REDUCING_ODDS_RATE'] = 0.005      # Rate were the odds of crossing over or mutating happen is reducing
settings['REDUCING_THRESHOLD'] = 0.09       # Threshold for the reducing odds
settings['TOP_ELITE_CROSSOVER_ODDS'] = 0.51 # Odds of crossing over with the top elite (odds goes down when goign down the list of elites)


def main():
    pygame.init()
    game = Game(settings)
    game.handle_game()

    time.sleep(1)
    pygame.quit()


# call the "main" function if running this script
if __name__ == '__main__': main()
