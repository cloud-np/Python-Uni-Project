from classes.design import Design
import numpy as np
from typing import Any


class Gordian:
    def __init__(self, design: Design):
        self.design: Design = design
        n_nodes: int = len(self.design.nodes)
        self.matrix: Any = np.zeros((n_nodes, n_nodes))
        self.populate_matrix()

    def populate_matrix(self):
        """Populate the matrix with correct weight values."""
        for net in self.design.nets:
            for node in net.nodes:
                for node2 in net.nodes:
                    if node is not node2:
                        n_ids = [node.gid, node2.gid]
                        weight = self.get_edge_weight(node, node2)
                        self.matrix[n_ids[0]][n_ids[1]] = weight
                        self.matrix[n_ids[1]][n_ids[0]] = weight
        print(self.matrix)
        pass

    def get_edge_weight(self, node, node2) -> float:
        """Find the edge weight between the two given nodes.

        Note that this function doesn't care if the edge
        between the 2 given nodes exists in the first place!
        The way it founds the correct weight its the following:
            if the 2 given nodes exist in a given net add 2 / k
            k = number of nodes in the given net.

        Args:
            node (Node): The first given Node.
            node2 (Node): The second given Node.

        Returns:
            float: Returns the weight of the edge.
        """
        # edge_weight = sum([2 / len(net.nodes) for net in self.design.nets if (node in net.nodes and node2 in net.nodes)])
        edge_weight = round(sum([2 / len(net.nodes) for net in self.design.nets if (node in net.nodes and node2 in net.nodes)]), 2)
        return edge_weight if edge_weight > 0 else 1
