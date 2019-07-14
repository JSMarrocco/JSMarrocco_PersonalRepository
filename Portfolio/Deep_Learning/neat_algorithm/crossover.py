from genome import Genome
from nodeGenes import NodeType

import random, copy


def crossover(genome_a: Genome, genome_b: Genome):
    child = Genome()
    maxInn = max(genome_a.connectionGenes.maxInnovationNumber, genome_b.connectionGenes.maxInnovationNumber)
    child.nodeGenes.nodes += genome_a.nodeGenes.get_nodes_by_type(NodeType.INPUT)
    child.nodeGenes.nodes += genome_a.nodeGenes.get_nodes_by_type(NodeType.OUTPUT)
    for i in range(1, maxInn + 1):
        if (not genome_a.connectionGenes.get_connection_by_innovation(i) and genome_b.connectionGenes.get_connection_by_innovation(i)) or\
                (genome_b.connectionGenes.get_connection_by_innovation(i) and genome_b.fitness > genome_a.fitness):
            child.add_gene(copy.deepcopy(genome_b.connectionGenes.get_connection_by_innovation(i)))
        elif (not genome_b.connectionGenes.get_connection_by_innovation(i) and genome_a.connectionGenes.get_connection_by_innovation(i)) or\
                (genome_a.connectionGenes.get_connection_by_innovation(i) and genome_a.fitness > genome_b.fitness):
            child.add_gene(copy.deepcopy(genome_a.connectionGenes.get_connection_by_innovation(i)))
        elif genome_a.connectionGenes.get_connection_by_innovation(i) and genome_b.connectionGenes.get_connection_by_innovation(i) and\
                genome_a.fitness == genome_b.fitness:
            child.add_gene(copy.deepcopy(random.choice([genome_a, genome_b]).connectionGenes.get_connection_by_innovation(i)))

    return child
