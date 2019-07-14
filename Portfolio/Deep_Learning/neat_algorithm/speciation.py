from genome import Genome

import random

THRESHOLD = 2.8
WEIGHT_NUMBER_DISJOINT_EXCESS = 0.6
WEIGHT_DIFFERENCE_WEIGHT = 0.4


def speciation(genomes: [Genome]):
    species = []

    for genome in genomes:
        if len(species) == 0:
            species.append([genome])
        else:
            same_specie_find = False
            for specie in species:
                same_specie_find = check_same_specie(random.choice(specie), genome)
                if same_specie_find:
                    specie.append(genome)
                    break
            if not same_specie_find:
                species.append([genome])

    return species


def elitism_species(species, elitism_level):
    elites_species = []
    for specie in species:
        if len(specie) <= 2:
            elites = specie
        else:
            specie = sorted(specie, key=lambda x: x.fitness, reverse=True)
            elites = specie[:int(len(specie) * elitism_level)]

        elites_species.append(elites)

    return elites_species


def check_same_specie(genome_a, genome_b):
    maxInn = max(genome_a.connectionGenes.maxInnovationNumber, genome_b.connectionGenes.maxInnovationNumber)
    sum_disjoint_excess = 0
    diff_weights = 0
    for i in range(1, maxInn + 1):
        if (not genome_a.connectionGenes.get_connection_by_innovation(i) and genome_b.connectionGenes.get_connection_by_innovation(i)) or\
                (not genome_b.connectionGenes.get_connection_by_innovation(i) and genome_a.connectionGenes.get_connection_by_innovation(i)):
            sum_disjoint_excess += 1
        elif genome_a.connectionGenes.get_connection_by_innovation(i) and genome_b.connectionGenes.get_connection_by_innovation(i):
            diff_weights += abs(genome_a.connectionGenes.get_connection_by_innovation(i).weight -
                                genome_b.connectionGenes.get_connection_by_innovation(i).weight)

    return (WEIGHT_NUMBER_DISJOINT_EXCESS * sum_disjoint_excess) +\
           (WEIGHT_DIFFERENCE_WEIGHT * diff_weights) <= THRESHOLD
