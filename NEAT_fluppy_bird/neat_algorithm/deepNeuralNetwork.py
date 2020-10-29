from enum import Enum
from genome import Genome
from nodeGenes import NodeType

import numpy as np
import math, queue


class ActivationFunctions(Enum):
    RELU = 'relu'
    SIGMOID = 'sigmoid'
    SOFTMAX = 'softmax'


class Neurone:
    def __init__(self, neurone_id, neurone_type):
        self.id = neurone_id
        self.value = None
        self.type = neurone_type

    def update_value(self, values, activation_function):
        z = 0
        for v in values:
            z += v['weight'] * v['value']

        self.value = use_correct_function(activation_function, z)


class DeepNeuralNetwork:
    def __init__(self, activation_function: ActivationFunctions, output_function: ActivationFunctions, genome: Genome):
        self.activationFunction = activation_function
        self.outputFunction = output_function
        self.neurones = {}
        self.__class_neuron_by_type(genome.nodeGenes)
        self.genome = genome

    def get_fitness(self):
        return self.genome.fitness

    def increment_fitness(self, value=1):
        self.genome.fitness += value

    def get_connections(self):
        return self.genome.connectionGenes

    def feed_forward(self, inputs):
        for i in range(len(inputs)):
            self.neurones[NodeType.INPUT][i].value = inputs[i]

        self.__update_value_neurones()

        outputs = []
        for neuron in self.neurones[NodeType.OUTPUT]:
            outputs.append(neuron.value)

        return use_correct_function(self.outputFunction, outputs)

    def __update_value_neurones(self):
        hidden_neuron_queue = queue.Queue()
        for neuron in self.neurones[NodeType.HIDDEN]:
            hidden_neuron_queue.put(neuron)
        for neuron in self.neurones[NodeType.OUTPUT]:
            hidden_neuron_queue.put(neuron)

        dead_neurones = set()
        contains_outputs = False
        loop_ptr = None
        while not hidden_neuron_queue.empty():
            n = hidden_neuron_queue.get()

            if n.type is NodeType.OUTPUT:
                contains_outputs = True
            if loop_ptr == n.id and not contains_outputs:
                return
            if not loop_ptr:
                loop_ptr = n.id

            input_connections = self.get_connections().get_enabled_connections_by_output(n)
            values = []
            if len(input_connections) < 1:
                dead_neurones.add(n.id)
            else:
                for connection in input_connections:
                    v = self.__get_neurone_by_id_and_type(connection.inNode.id, connection.inNode.type).value
                    if connection.inNode.id in dead_neurones and values == []:
                        dead_neurones.add(n.id)
                    elif v is None and connection.inNode.id not in dead_neurones:
                        values = []
                        hidden_neuron_queue.put(n)
                        break
                    elif v is not None and connection.inNode.id not in dead_neurones:
                        if n.id in dead_neurones:
                            dead_neurones.remove(n.id)
                        values.append({'weight': connection.weight, 'value': v})

                if values:
                    loop_ptr = None
                    n.update_value(values, self.activationFunction)

    def __class_neuron_by_type(self, nodes):
        self.neurones = {NodeType.INPUT: [], NodeType.HIDDEN: [], NodeType.OUTPUT: []}
        for node in nodes.get_nodes_by_type(NodeType.INPUT):
            self.neurones[NodeType.INPUT].append(Neurone(node.id, NodeType.INPUT))

        for node in nodes.get_nodes_by_type(NodeType.HIDDEN):
            self.neurones[NodeType.HIDDEN].append(Neurone(node.id, NodeType.HIDDEN))

        for node in nodes.get_nodes_by_type(NodeType.OUTPUT):
            self.neurones[NodeType.OUTPUT].append(Neurone(node.id, NodeType.OUTPUT))

    def __get_neurone_by_id_and_type(self, id, type):
        return next((x for x in self.neurones[type] if x.id == id), None)


def use_correct_function(activation_function: ActivationFunctions, value):
    if activation_function == ActivationFunctions.RELU:
        return relun(value)
    elif activation_function == ActivationFunctions.SIGMOID:
        return sigmoid(value)
    elif activation_function == ActivationFunctions.SOFTMAX:
        if not isinstance(value, list):
            value = [value]
        return softmax(value)


def relun(value):
    return max(0, value)


def softmax(values):
    e_x = []
    for value in values:
        if not value is None:
            e_x.append(np.exp(value))

    normalize_vector = []
    for value in e_x:
        normalize_vector.append(value / sum(e_x))

    return normalize_vector


def sigmoid(value):
    return 1 / (1 + math.exp(-value))
