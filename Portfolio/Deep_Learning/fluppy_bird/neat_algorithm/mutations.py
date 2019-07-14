from nodeGenes import NodeType
from genome import Genome

import random


def point_mutation(genome: Genome):
    connection = random.choice(genome.connectionGenes.connections)
    connection.weight = random.uniform(-2, 2)


def link_mutation(genome: Genome):
    input_node, output_node = genome.nodeGenes.get_two_random_nodes()
    options_count_max = calculate_nb_possible_link(genome)
    combination = set()
    while genome.connectionGenes.get_connection_by_input_and_output_nodes(input_node, output_node) or \
            genome.connectionGenes.get_connection_by_input_and_output_nodes(output_node, input_node):
        if len(combination) >= options_count_max:
            return
        else:
            combination.add(str(input_node.id) + '-' + str(output_node.id))
            input_node, output_node = genome.nodeGenes.get_two_random_nodes()

    genome.connectionGenes.add_new_connection(input_node, output_node, random.uniform(-2, 2))


def node_mutation(genome: Genome):
    connection_gene = random.choice(genome.connectionGenes.connections)
    new_node_id = genome.nodeGenes.add_new_node(NodeType.HIDDEN)[0]

    connection_gene.enabled = False
    genome.connectionGenes.add_new_connection(connection_gene.inNode, genome.nodeGenes.get_node_by_id(new_node_id), 1)
    genome.connectionGenes.add_new_connection(genome.nodeGenes.get_node_by_id(new_node_id), connection_gene.outNode, connection_gene.weight)


def enabled_mutation(genome: Genome):
    connection_gene = random.choice(genome.connectionGenes.connections)
    connection_gene.enabled = False


def random_mutation(genome: Genome):
    mutation_id = random.randint(1, 4)
    if mutation_id == 1:
        point_mutation(genome)
    elif mutation_id == 2:
        link_mutation(genome)
    elif mutation_id == 3:
        node_mutation(genome)
    elif mutation_id == 4:
        enabled_mutation(genome)


def calculate_nb_possible_link(genome):
    nodes_count = {'INPUT': len(genome.nodeGenes.get_nodes_by_type(NodeType.INPUT)),
                   'HIDDEN': len(genome.nodeGenes.get_nodes_by_type(NodeType.HIDDEN)),
                   'OUTPUT': len(genome.nodeGenes.get_nodes_by_type(NodeType.OUTPUT))}
    options_count_max = (nodes_count['INPUT'] + nodes_count['HIDDEN'] - 1) * nodes_count['HIDDEN'] + \
                        (nodes_count['INPUT'] + nodes_count['HIDDEN']) * nodes_count['OUTPUT']
    return options_count_max
