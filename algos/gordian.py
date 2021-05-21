from classes.design import Design
from classes.node import Node
import numpy as np
from typing import Any, List


class Gordian:
    def __init__(self, design: Design):
        self.design: Design = design
        num_cnodes: int = len(self.design.c_nodes)
        self.cell_matrix: Any = np.zeros((num_cnodes, num_cnodes))
        # pin-connection matrix n x m:
        # n = number of cell nodes
        # m = number of terminal nodes
        self.pin_matrix: Any = np.zeros((len(self.design.c_nodes), len(self.design.t_nodes)))
        self.__populate_cell_and_pin_matrixs()
        self.degree_matrix: np.ndarray = self.__create_degree_matrix()

    def __create_degree_matrix(self) -> np.ndarray:
        cell_matrix_sum: np.ndarray = np.sum(self.cell_matrix, axis=1)
        pin_matrix_sum: np.ndarray = np.sum(self.pin_matrix, axis=1)
        rows_sum: np.ndarray = cell_matrix_sum + pin_matrix_sum

        num_cnodes: int = len(self.design.c_nodes)
        degree_matrix: np.ndarray = np.zeros((num_cnodes, num_cnodes))
        np.fill_diagonal(degree_matrix, rows_sum)
        print(degree_matrix)

        return degree_matrix

    def __populate_cell_and_pin_matrixs(self):
        """Populate the correct matrix with correct weight values."""

        def populate(matrix: np.ndarray, nodes_arr: List[Node]):
            for node in nodes_arr:
                for node2 in self.design.c_nodes:
                    if node is node2:
                        continue
                    for net in self.design.nets:
                        if (node in net.nodes and node2 in net.nodes):
                            n_ids = [node.gid, node2.gid]
                            weight = self.__get_edge_weight(node, node2)
                            matrix[n_ids[0]][n_ids[1]] = weight
                            matrix[n_ids[1]][n_ids[0]] = weight
        populate(self.cell_matrix, self.design.c_nodes)
        populate(self.pin_matrix, self.design.t_nodes)

    def __get_edge_weight(self, node, node2) -> float:
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
        # With no round().
        # edge_weight = sum([2 / len(net.nodes) for net in self.design.nets if (node in net.nodes and node2 in net.nodes)])
        edge_weight = round(sum([2 / len(net.nodes) for net in self.design.nets if (node in net.nodes and node2 in net.nodes)]), 2)
        return edge_weight if edge_weight > 0 else 1
