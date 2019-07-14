from crossover import crossover
from mutations import random_mutation, point_mutation
from speciation import speciation, elitism_species
from nodeGenes import NodeGenes, NodeType
from genome import Genome

import copy, random

DEFAULT_SETTINGS = {'ELITISM': 0.67,                    # Percentage of elites in a specie (The ones that will be allow to reproduce)
                    'CROSSOVER_ODDS': 0.6,              # Odds of genomes reproducing with another one
                    'MUTATION_ODDS': 1,                 # Odds of genomes mutating if not reproducing with another one
                    'REDUCING_ODDS_RATE':  0.01,        # Rate were the odds of crossing over or mutating happen is reducing
                    'REDUCING_THRESHOLD': 0.1,          # Threshold for the reducing odds
                    'TOP_ELITE_CROSSOVER_ODDS': 0.51}   # Threshold for the reducing odds


class Genomes:
    def __init__(self, amount_input, amount_output, amount_genomes, settings=DEFAULT_SETTINGS):
        self.genomes = []
        self.settings = settings
        self.init_genomes(amount_input, amount_output, amount_genomes)

    def init_genomes(self, amount_input, amount_output, amount_genomes):
        node_genes = NodeGenes()
        node_genes.add_new_node(NodeType.INPUT, amount_input)
        node_genes.add_new_node(NodeType.OUTPUT, amount_output)

        self.genomes = []
        for i in range(amount_genomes):
            self.genomes.append(Genome())
            new_genome = self.genomes[i]
            self.__init_new_genome(new_genome, node_genes)

    def __init_new_genome(self, new_genome, node_genes):
        new_genome.nodeGenes = node_genes
        output_nodes = node_genes.get_nodes_by_type(NodeType.OUTPUT)
        for output_node in output_nodes:
            input_node = random.choice(node_genes.get_nodes_by_type(NodeType.INPUT))
            while new_genome.connectionGenes.get_connection_by_input_and_output_nodes(input_node, output_node) or \
                    new_genome.connectionGenes.get_connection_by_input_and_output_nodes(output_node, input_node):
                input_node = random.choice(node_genes.get_nodes_by_type(NodeType.INPUT))

            find_same_connection = False
            for genome in self.genomes:
                connection = genome.connectionGenes.get_connection_by_input_and_output_nodes(input_node,
                                                                                             output_node)
                if connection:
                    new_genome.connectionGenes.add_existing_connection(copy.deepcopy(connection))
                    point_mutation(new_genome)
                    find_same_connection = True
                    break

            if not find_same_connection:
                new_genome.connectionGenes.add_new_connection(input_node, output_node, random.uniform(-2, 2))

    def evolve(self):
        species = speciation(self.genomes)
        species = elitism_species(species, self.settings['ELITISM'])

        elites_poll = []
        for specie in species:
            elites_poll += specie
        elites_poll = sorted(elites_poll, key=lambda x: x.fitness, reverse=True)

        self.genomes[0].fitness = 0
        new_genomes = [copy.deepcopy(elites_poll[0])]

        for elite in elites_poll:
            self.__evolve_genome(copy.deepcopy(elite), new_genomes, [x for x in elites_poll if x != elite])

        genome_amount = len(self.genomes) - len(new_genomes)
        if genome_amount > 0:
            self.__add_missing_genomes(genome_amount, new_genomes, species)

        self.genomes = new_genomes

        self.__update_evolution_settings()

    def __update_evolution_settings(self):
        if self.settings['REDUCING_THRESHOLD'] > 0:
            self.settings['REDUCING_THRESHOLD'] -= self.settings['REDUCING_ODDS_RATE']
            self.settings['CROSSOVER_ODDS'] = self.settings['CROSSOVER_ODDS'] - self.settings['REDUCING_ODDS_RATE']
            self.settings['MUTATION_ODDS'] = self.settings['MUTATION_ODDS'] - self.settings['REDUCING_ODDS_RATE'] * 4

    def __evolve_genome(self, new_genome, new_genomes, elites):
        if random.uniform(0, 1) <= self.settings['CROSSOVER_ODDS']:
            second_parent = self.__choose_random_genome_by_elite(elites)
            while second_parent == new_genome:
                second_parent = self.__choose_random_genome_by_elite(elites)
            new_genome = crossover(new_genome, second_parent)
        elif random.uniform(0, 1) <= self.settings['MUTATION_ODDS']:
            random_mutation(new_genome)
        new_genome.fitness = 0
        new_genomes.append(new_genome)

    def __add_missing_genomes(self, amount, new_genomes, species):
        top_elites = []
        for specie in species:
            top_elites.append(specie[0])

        for _ in range(amount):
            new_genome = copy.deepcopy(random.choice(top_elites))
            new_genome.fitness = 0
            if len(top_elites) == 1:
                if random.uniform(0, 1) <= self.settings['MUTATION_ODDS']:
                    random_mutation(new_genome)
                new_genomes.append(new_genome)
            else:
                self.__evolve_genome(new_genome, new_genomes, top_elites)

    def __choose_random_genome_by_elite(self, elites):
        if random.uniform(0, 1) <= self.settings['TOP_ELITE_CROSSOVER_ODDS']:
            return elites[0]
        else:
            for i in range(1, len(elites)):
                if random.uniform(0, 1) <= (1 - self.settings['TOP_ELITE_CROSSOVER_ODDS'])/i:
                    return elites[i]

        return elites[0]



