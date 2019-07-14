from enum import Enum

import random


nodes_count = 0


class NodeType(Enum):
    INPUT = 'input'
    OUTPUT = 'output'
    HIDDEN = 'hidden'


class NodeGene:
    def __init__(self, node_id, node_type: NodeType):
        self.id = node_id
        self.type = node_type


class NodeGenes:
    def __init__(self):
        self.nodes = []

    def get_node_by_id(self, id):
        return next((x for x in self.nodes if x.id == id), None)

    def get_nodes_by_type(self, type: NodeType):
        return [x for x in self.nodes if x.type == type]

    def get_two_random_nodes(self):
        input_node = random.choice(self.nodes)
        while input_node.type == NodeType.OUTPUT:
            input_node = random.choice(self.nodes)

        output_node = random.choice(self.nodes)
        while output_node == input_node or output_node.type == NodeType.INPUT:
            output_node = random.choice(self.nodes)

        return input_node, output_node

    def possess_node(self, node_id):
        return node_id in self.nodes.keys()

    def add_new_node(self, node_type, amount=1):
        new_id = []
        for _ in range(amount):
            global nodes_count
            nodes_count += 1
            node_id = nodes_count
            new_id.append(node_id)
            self.nodes.append(NodeGene(node_id, node_type))

        return new_id

    def add_existing_node(self, node: NodeGene):
        if not self.get_node_by_id(node.id):
            self.nodes.append(node)
