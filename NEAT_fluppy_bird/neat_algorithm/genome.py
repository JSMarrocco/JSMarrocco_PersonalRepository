from nodeGenes import NodeGenes
from connectionGenes import ConnectionGenes

import copy


class Genome:
    def __init__(self):
        self.nodeGenes = NodeGenes()
        self.connectionGenes = ConnectionGenes()
        self.fitness = 0

    def add_gene(self, new_connection):
        self.nodeGenes.add_existing_node(new_connection.inNode)
        self.nodeGenes.add_existing_node(new_connection.outNode)
        self.connectionGenes.add_existing_connection(copy.deepcopy(new_connection))
