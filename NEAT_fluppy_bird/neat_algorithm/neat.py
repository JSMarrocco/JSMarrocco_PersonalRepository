from genomes import Genomes

from deepNeuralNetwork import DeepNeuralNetwork, ActivationFunctions
import random

DEFAULT_SETTINGS = {'ELITISM': 0.67,                    # Percentage of elites in a specie (The ones that will be allow to reproduce)
                    'CROSSOVER_ODDS': 0.6,              # Odds of genomes reproducing with another one
                    'MUTATION_ODDS': 1,                 # Odds of genomes mutating if not reproducing with another one
                    'REDUCING_ODDS_RATE':  0.01,        # Rate were the odds of crossing over or mutating happen is reducing
                    'REDUCING_THRESHOLD': 0.1,          # Threshold for the reducing odds
                    'TOP_ELITE_CROSSOVER_ODDS': 0.51}   # Odds of crossing over with the top elite (odds goes down when goign down the list of elites)


def main():

    # 1. Initialize first genomes poll
    genomes_poll = Genomes(3, 2, 5, DEFAULT_SETTINGS)

    # 2. Assigned deep neural network to some entities with a genomes
    dnns = []
    for genome in genomes_poll.genomes:
        dnns.append(DeepNeuralNetwork(ActivationFunctions.RELU, ActivationFunctions.SOFTMAX, genome))

    print_genomes(genomes_poll)

    for dnn in dnns:
        # 3. Get outputs values with feed_forward function of deep neural network
        dnn.feed_forward([100, 50, -20])
        # 4. Assigned fitness to the neural network genome
        dnn.genome.fitness = random.randint(0, 20)

    # 5. Update genomes poll with deep neural network genome with fitness value
    genomes_poll.genomes = []
    for dnn in dnns:
        genomes_poll.genomes.append(dnn.genome)

    # 6. Evolve genomes poll
    genomes_poll.evolve()

    # 7. Assigned evolved genomes to deep neural network
    dnns = []
    for genome in genomes_poll.genomes:
        dnns.append(DeepNeuralNetwork(ActivationFunctions.RELU, ActivationFunctions.SOFTMAX, genome))

    # 8. Repeat to point 3.

    print_genomes(genomes_poll)


def print_genomes(genomes_poll):
    print('-----')
    for genome in genomes_poll.genomes:
        for c in genome.connectionGenes.connections:
            print(str(c.inNode.id) + '|' + str(c.outNode.id) + '|' + str(c.weight) + '|' + str(
                c.innovation) + '|' + str(c.enabled))
        print('')


if __name__ == '__main__': main()
