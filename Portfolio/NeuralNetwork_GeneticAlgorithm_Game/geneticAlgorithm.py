import pygame, math, copy
from player import Player
from random import sample, uniform, randint

SCREENRECT = pygame.Rect(0, 0, 640, 580)

def evolve(settings, organismsOld, gen, oldScore):
    '''
        1. Sorted the old organisms with their fitness value
        2. Past the top organism directly to the next gen ( ex: top 3)
        3. Select 2 organisms to crossover
            3a. organism 1 has 100% chance of being from the top organisms
            3b. organism 2 has more chance of coming from the top but has
                a some chance of coming from 'ok' organisms
            3c. The worst organisms have 0% chance of crossover
        4. Crossover the weights/biases of the two organisms
            4a. crossover = (crossover_bias * value1) + ((1 - crossover_bias) * value2))
            4b. Every weights/biases has a % of chance of crossover or keeping the value from organism 1
            4c. Every weights/biases has a % of mutating (random value)
        5. Repeat #4 for the number of space left in new organisms array - 1 space
        6. Give the last place to a random generated organism to keep the organism list new

    :param settings: evolution setting
    :param organismsOld: old organisms that need to evolve
    :param gen: last generation
    :param oldScore: best score yet
    :return: new organisms that evolved
    '''
    elitismNum = int(math.floor(settings['ELITISM'] * settings['POPULATION_SIZE']))
    newOrgs = settings['POPULATION_SIZE'] - elitismNum

    # --- Elitism (Keep best performing) ---#
    orgsSorted = sorted(organismsOld, key=lambda x: x.fitness, reverse=False)
    if orgsSorted[0].fitness == 0:
        return [Player(SCREENRECT.centerx, 430, 5, 5, orgsSorted[0].color, orgsSorted[0].goal,
                       orgsSorted[0].obstacles, orgsSorted[0].brain)], gen, orgsSorted[0].fitness
    elif orgsSorted[0].fitness < oldScore:
        orgsSorted[0].color = (randint(50, 200), randint(50, 200), randint(50, 200))

    organismsNew = []
    for i in range(0, elitismNum):
        organismsNew.append(
            Player(SCREENRECT.centerx, 430, 5, 5, orgsSorted[i].color, orgsSorted[i].goal, orgsSorted[i].obstacles,
                   orgsSorted[i].brain)
        )

    # --- Generate new population ---#
    for w in range(0, newOrgs - 1):

        # Selection
        candidates = list(range(0, elitismNum))
        randomIndex = sample(candidates, 1)
        org_1 = copy.deepcopy(orgsSorted[randomIndex[0]])

        crossOdds = uniform(0, 1)
        if crossOdds <= settings['REPRODUCE_ODDS']:
            randomIndex = sample(candidates, 1)
            org_2 = copy.deepcopy(orgsSorted[randomIndex[0]])
        else:
            candidates = list(range(elitismNum, int(newOrgs * (settings['ELITISM'] + 0.3)))) if newOrgs * (
                    settings['ELITISM'] + 0.1) >= 2 else list(range(0, 2))
            randomIndex = sample(candidates, 1)
            org_2 = copy.deepcopy(orgsSorted[randomIndex[0]])

        # Crossover
        newPlayer = Player(SCREENRECT.centerx, 430, 5, 5, org_1.color, org_1.goal, org_1.obstacles, org_1.brain)
        for i in range(0, len(org_1.brain.hiddenLayers)):
            for j in range(0, len(org_1.brain.hiddenLayers[i])):

                if uniform(0, 1) <= settings['CROSSOVER_ODDS']:
                    crossBias = uniform(0, 1)
                    newBias = (crossBias * org_1.brain.hiddenLayers[i][j]['bias']) + \
                               ((1 - crossBias) * org_2.brain.hiddenLayers[i][j]['bias'])
                else:
                    newBias = org_1.brain.hiddenLayers[i][j]['bias']

                if uniform(0, 1) > settings['MUTATION_ODDS']: newBias = uniform(-1, 1)

                newWeights = []

                for k in range(0, len(org_1.brain.hiddenLayers[i][j]['weights'])):

                    if uniform(0, 1) <= settings['CROSSOVER_ODDS']:

                        crossWeight = uniform(0, 1)
                        tmpWeight = (crossWeight * org_1.brain.hiddenLayers[i][j]['weights'][k]) + \
                                    ((1 - crossWeight) * org_2.brain.hiddenLayers[i][j]['weights'][k])

                    else:
                        tmpWeight = org_1.brain.hiddenLayers[i][j]['weights'][k]

                    if uniform(0, 1) <= settings['MUTATION_ODDS']: tmpWeight = uniform(-1, 1)

                    newWeights.append(tmpWeight)

                newPlayer.brain.hiddenLayers[i][j]['bias'] = newBias
                newPlayer.brain.hiddenLayers[i][j]['weights'] = newWeights

        organismsNew.append(newPlayer)

    organismsNew.append(Player(SCREENRECT.centerx, 430, 5, 5,
                                (randint(50, 200), randint(50, 200), randint(50, 200)),
                                organismsNew[0].goal,
                                organismsNew[0].obstacles))
    gen += 1
    return organismsNew, gen, orgsSorted[0].fitness