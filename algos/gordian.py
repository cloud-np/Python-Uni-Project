from classes.design import Design
from classes.node import Node
import numpy as np
from cvxopt import matrix, solvers
from data.gordian_example import cell_matrix, pin_matrix, fixed_pin_x, fixed_pin_y
from typing import Any, List, Tuple


class Gordian:
    def __init__(self, design: Design, load_example: bool = False):
        if not load_example:
            self.design: Design = design
            num_cnodes: int = len(self.design.c_nodes)

            self.pin_matrix: Any = np.zeros((num_cnodes, len(self.design.t_nodes)))
            self.cell_matrix: Any = np.zeros((num_cnodes, num_cnodes))
            self.__populate_cell_and_pin_matrixs()

            self.fixed_pin_x, self.fixed_pin_y = self.__create_fixed_pin_vectors()
        else:
            self.pin_matrix, self.cell_matrix = pin_matrix, cell_matrix
            self.fixed_pin_x, self.fixed_pin_y = fixed_pin_x, fixed_pin_y
        self.degree_matrix: np.ndarray = self.__create_degree_matrix()
        self.laplacian_matrix: np.ndarray = self.degree_matrix - self.cell_matrix

    @staticmethod
    def find_middle_point(xs: Tuple[float], ys: Tuple[float]) -> Tuple[float]:
        return ([(xs[0] + xs[1]) / 2, (ys[0] + ys[1]) / 2])

    def create_subpartitions_border_points(self, first_point: np.array, second_point: np.array):
        x_mid = (first_point[0] + second_point[0]) / 2
        return [first_point[0], x_mid], [x_mid, second_point[0]]

    def create_subpartitions(self):
        last_row = len(self.design.rows) - 1
        x1, y1 = self.design.rows[0].x_end, self.design.rows[0].y
        x2, y2 = self.design.rows[last_row].x, self.design.rows[last_row].y_end
        self.create_subpartitions_border_points(np.array([x1, y1]), np.array[x2, y2])

    def solve_qp(self):
        # .T means transponse e.g: [[1, 2], [3, 4]].T => [[1, 3]]
        #                                                 [2, 4]]
        C = .5 * (self.laplacian_matrix + self.laplacian_matrix.T)
        args = [matrix(C), matrix(fixed_pin_x)]
        sol = solvers.qp(*args)
        return np.array(sol['x']).reshape((C.shape[1]))

    def __create_fixed_pin_vectors(self) -> Tuple[np.ndarray, np.ndarray]:
        pin_x_pos, pin_y_pos = [pin.x for pin in self.design.t_nodes], [pin.y for pin in self.design.t_nodes]

        # We use "-1 *" just to make it a bit more readable.
        fixed_pin_x = np.array([-1 * np.sum(self.pin_matrix[i] * pin_x_pos[i]) for i in range(len(self.design.t_nodes))])
        fixed_pin_y = np.array([-1 * np.sum(self.pin_matrix[i] * pin_y_pos[i]) for i in range(len(self.design.t_nodes))])
        return fixed_pin_x, fixed_pin_y

    def __create_degree_matrix(self) -> np.ndarray:
        cell_matrix_sum: np.ndarray = np.sum(self.cell_matrix, axis=1)
        pin_matrix_sum: np.ndarray = np.sum(self.pin_matrix, axis=1)
        rows_sum: np.ndarray = cell_matrix_sum + pin_matrix_sum

        # We can't use "matrix.size" because the matrix may be loaded from examples aka a List
        num_cnodes: int = len(self.cell_matrix[0])
        degree_matrix: np.ndarray = np.zeros((num_cnodes, num_cnodes))
        np.fill_diagonal(degree_matrix, rows_sum)

        return degree_matrix

    def __populate_cell_and_pin_matrixs(self) -> None:
        """Populate the correct matrix with correct weight values."""

        def populate(matrix: np.ndarray, nodes_arr: List[Node]):
            for node in nodes_arr:
                for node2 in self.design.c_nodes:
                    if node is node2:
                        continue
                    # NOTE:
                    # Although this makes more sense and its faster
                    # we assign values even to nodes that are not correlated
                    # weight = self.__get_edge_weight(node, node2)
                    # matrix[node.gid][node2.gid] = weight
                    # matrix[node2.gid][node.gid] = weight
                    for net in self.design.nets:
                        if (node in net.nodes and node2 in net.nodes):
                            weight = self.__get_edge_weight(node, node2)
                            matrix[node.gid][node2.gid] = weight
                            matrix[node2.gid][node.gid] = weight
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
        edge_weight = sum(
            2 / len(net.nodes)
            for net in self.design.nets
            if (node in net.nodes and node2 in net.nodes)
        )
        # edge_weight = round(sum(2 / len(net.nodes) for net in self.design.nets if (node in net.nodes and node2 in net.nodes)), 2)
        return edge_weight if edge_weight > 0 else 1
