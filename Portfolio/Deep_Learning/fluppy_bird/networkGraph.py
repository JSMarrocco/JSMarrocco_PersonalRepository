from gameObject import GameObject

import pygame, sys

sys.path.insert(0, './neat_algorithm')
from genome import Genome
from nodeGenes import NodeGenes, NodeType

GRAPH_NODE_RADIUS = 15
GRAPH_NODE_COLOR = (255, 80, 80)
COLOR_GREY = (77, 77, 77)


class GraphNode(GameObject):
    def __init__(self, x, y, id):
        GameObject.__init__(self, x, y, GRAPH_NODE_RADIUS, GRAPH_NODE_RADIUS)
        self.color = GRAPH_NODE_COLOR
        self.id = id

    def draw(self, surface, font, radius = GRAPH_NODE_RADIUS):
        pygame.draw.circle(surface, self.color, (self.bounds.x, self.bounds.y), self.bounds.height, self.bounds.width)
        surface.blit(font.render(str(self.id), 1, COLOR_GREY),
                     (self.bounds.x - radius/3, self.bounds.y - radius))


class GraphConnection:
    def __init__(self, start_pos, end_pos, weight):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.weight = weight

    def draw(self, surface):
        width = int(1 + abs(2 * self.weight))
        color = 255 - abs(125*self.weight)
        pygame.draw.line(surface, (color, color, color), self.start_pos, self.end_pos, width)


class NetworkGraph:
    def __init__(self):
        self.graphNodes = []
        self.graphConnection = []
        self.frame_size = 0

    def set_graph(self, genome: Genome):
        self.graphNodes = []
        self.graphConnection = []

        for i, node in enumerate(genome.nodeGenes.get_nodes_by_type(NodeType.INPUT)):
            self.graphNodes.append(GraphNode(550, 242 + (GRAPH_NODE_RADIUS * 4 * i), node.id))
        for i, node in enumerate(genome.nodeGenes.get_nodes_by_type(NodeType.HIDDEN)):
            self.graphNodes.append(GraphNode(725, 242 + (GRAPH_NODE_RADIUS * 4 * i), node.id))
        for i, node in enumerate(genome.nodeGenes.get_nodes_by_type(NodeType.OUTPUT)):
            self.graphNodes.append(GraphNode(900, 242 + (GRAPH_NODE_RADIUS * 4 * i), node.id))

        self.__set_frame_size(genome)

        for connection in genome.connectionGenes.get_enabled_connections():
            start_node = self.__get_grahNode_by_id(connection.inNode.id)
            end_node = self.__get_grahNode_by_id(connection.outNode.id)
            self.graphConnection.append(GraphConnection((start_node.bounds.x, start_node.bounds.y),
                                                        (end_node.bounds.x, end_node.bounds.y),
                                                        connection.weight))

    def draw(self, surface):
        font = pygame.font.SysFont("arial", 24)
        if self.graphNodes and self.graphConnection:
            surface.blit(font.render('Inputs', 1, COLOR_GREY), (526, 190))
            surface.blit(font.render('Hidden', 1, COLOR_GREY), (695, 190))
            surface.blit(font.render('Outputs', 1, COLOR_GREY), (876, 190))
            pygame.draw.rect(surface, COLOR_GREY, pygame.Rect(530, 222, 40, self.frame_size), 2)
            pygame.draw.rect(surface, COLOR_GREY, pygame.Rect(705, 222, 40, self.frame_size), 2)
            pygame.draw.rect(surface, COLOR_GREY, pygame.Rect(880, 222, 40, self.frame_size), 2)

        for connection in self.graphConnection:
            connection.draw(surface)
        for node in self.graphNodes:
            node.draw(surface, font)

    def __set_frame_size(self, genome):
        self.frame_size = len(genome.nodeGenes.get_nodes_by_type(NodeType.INPUT))
        if len(genome.nodeGenes.get_nodes_by_type(NodeType.OUTPUT)) > self.frame_size:
            self.frame_size = len(genome.nodeGenes.get_nodes_by_type(NodeType.OUTPUT))
        elif len(genome.nodeGenes.get_nodes_by_type(NodeType.HIDDEN)) > self.frame_size:
            self.frame_size = len(genome.nodeGenes.get_nodes_by_type(NodeType.HIDDEN))

        self.frame_size *= GRAPH_NODE_RADIUS * 4

    def __get_grahNode_by_id(self, id):
        return next((x for x in self.graphNodes if x.id == id), None)
