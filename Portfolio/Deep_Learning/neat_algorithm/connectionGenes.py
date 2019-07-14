from nodeGenes import NodeGene

innovation_count = 1


class ConnectionGene:
    def __init__(self, input_node, output_node, weight, enabled=True):
        self.inNode: NodeGene = input_node
        self.outNode: NodeGene = output_node
        self.weight = weight
        self.innovation = innovation_count
        self.enabled = enabled


class ConnectionGenes:
    def __init__(self):
        self.connections = []
        self.maxInnovationNumber = innovation_count

    def get_connection_by_input_and_output_nodes(self, input_node, output_node):
        return next((x for x in self.connections if x.inNode.id == input_node.id and x.outNode.id == output_node.id), None)

    def get_connection_by_innovation(self, innovation):
        return next((x for x in self.connections if x.innovation == innovation), None)

    def get_enabled_connections_by_output(self, output_node):
        return [x for x in self.connections if x.outNode.id == output_node.id and x.enabled]

    def add_new_connection(self, input_node, output_node, weight, enabled=True):
        global innovation_count
        innovation_count += 1
        self.maxInnovationNumber = innovation_count
        self.connections.append(ConnectionGene(input_node, output_node, weight, enabled))

    def add_existing_connection(self, connection):
        if not self.get_connection_by_input_and_output_nodes(connection.inNode, connection.outNode) and\
           not self.get_connection_by_input_and_output_nodes(connection.outNode, connection.inNode):
            self.connections.append(connection)
