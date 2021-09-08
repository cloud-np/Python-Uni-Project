from classes.design import Design
from classes.node import Node
import numpy as np
from cvxopt import matrix, solvers
from data.gordian_example import cell_matrix, pin_matrix, fixed_pin_x, fixed_pin_y
from typing import List, Tuple


class Partition:
    def __init__(self, _id: int, cells: List[Node], border_xs: np.array, border_ys) -> None:
        self.id: int = _id
        self.cells: List[Node] = cells
        self.border_xs: np.array = border_xs
        self.border_ys: np.array = border_ys
        self.center: np.array = np.array([(self.border_xs[0] + self.border_xs[1]) / 2, (self.border_ys[0] + self.border_ys[1]) / 2])

    def __len__(self) -> int:
        return len(self.cells)

    @staticmethod
    def create_initial_partitions(cells, rows) -> Tuple['Partition']:
        # We sort by the x attr
        sorted_cells: List[Node] = sorted(cells, key=lambda c: c.x)
        sc_half: int = len(sorted_cells) // 2
        f_half_c: List[Node] = sorted_cells[:sc_half]
        s_half_c: List[Node] = sorted_cells[sc_half:]
        # We initially make the cut in the Y axis.
        border_xs, border_xs2 = Partition.__create_subparts_borders(rows[0].x, rows[len(rows) - 1].x_end)
        return Partition(0, cells=f_half_c, border_xs=border_xs, border_ys=np.array((0, 800))), Partition(1, cells=s_half_c, border_xs=border_xs2, border_ys=np.array((0, 800)))

    @staticmethod
    def get_uxys_from_parts(partitions: List['Partition']) -> Tuple[List[int]]:
        ux = [p.center[0] for p in partitions]
        uy = [p.center[1] for p in partitions]
        return ux, uy

    @staticmethod
    def __create_subparts_borders(p1: int, p2: int) -> Tuple[np.array]:
        mid = (p1 + p2) / 2
        return np.array([p1, mid]), np.array([mid, p2])

    @staticmethod
    def find_cells_in_area(partition: 'Partition', cells: List[Node], area: Tuple[np.array, np.array]) -> List[Node]:
        borders_x, borders_y = area
        # E.g: c.x = 15, c.y = 55, area = xs-(0, 50), ys-(0, 800)
        # 15 >= 0 and 15 <= 50  ---> True
        # 55 >= 0 and 55 <= 800 ---> True   That means that cell "c" is indeed in the area.
        return [c for c in cells if (borders_x[0] <= c.x <= borders_x[1]) and ((borders_y[0] <= c.y <= borders_y[1]))]

    def create_sub_partitions(self, seperate_on_y: bool) -> Tuple['Partition']:
        """Create sub partitions from this part.

        Parameters
        ----------
        seperate_on_y : bool
            Dictates if the seperation of the current partition will happen on the y axis.

        Returns
        -------
        Tuple[Partition]
            The sub partitions created from the current partition.
        """
        if seperate_on_y:
            borders_x, borders_x2 = Partition.__create_subparts_borders(*self.border_xs)
            borders_y = self.border_ys
            borders_y2 = self.border_ys
        else:
            borders_x = self.border_xs
            borders_x2 = self.border_xs
            borders_y, borders_y2 = Partition.__create_subparts_borders(*self.border_ys)

        cells = Partition.find_cells_in_area(partition=self, cells=self.cells, area=(borders_x, borders_y))
        cells2 = Partition.find_cells_in_area(partition=self, cells=self.cells, area=(borders_x2, borders_y2))
        return Partition(self.id + 1, cells=cells, border_xs=borders_x, border_ys=borders_y), Partition(self.id + 2, cells=cells2, border_xs=borders_x2, border_ys=borders_y2)


class Gordian:
    def __init__(self, design: Design, load_example: bool = False):
        if not load_example:
            self.design: Design = design
            num_cnodes: int = len(self.design.c_nodes)

            self.pin_matrix: np.ndarray = np.zeros(
                (num_cnodes, len(self.design.t_nodes)))
            self.cell_matrix: np.ndarray = np.zeros((num_cnodes, num_cnodes))
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

    def stopping_cond_met(self, partitions: List[Node]) -> bool:
        return any(len(p) < 2 for p in partitions)

    def run(self) -> None:
        partitions = Partition.create_initial_partitions(self.design.c_nodes, self.design.rows)
        n_cells = len(self.design.c_nodes)
        # At first the A matrix has only 2 rows since our partitions are only 2.
        A: np.ndarray = np.zeros((2, n_cells))
        A[0][:len(partitions[0]) - 1] = 1 / len(partitions[0])
        A[1][len(partitions[1]) - 1:] = 1 / len(partitions[1])
        # ux and uy from the centers from the partitions
        # ux: np.array = np.array([partitions[0].center[0], partitions[1].center[0]])
        # uy: np.array = np.array([partitions[0].center[1], partitions[1].center[1]])

        self.solve_qp_with_new_subject()
        seperate_on_y = False
        while not self.stopping_cond_met(partitions):
            # Get new subpartitions from current partitions
            partitions: List[Tuple[Partition]] = [p.create_sub_partitions(seperate_on_y) for p in partitions]
            # This is done to unpack the tuples inside the list because each
            # partitions gives us back a tuple of two subsparts. This operation
            # is called 'flatten' in other languages.
            partitions = sum(partitions, ())
            seperate_on_y = not seperate_on_y
            ux, uy = Partition.get_uxys_from_parts(partitions)
            # Create the A matrix
            A: np.ndarray = np.zeros([len(partitions), n_cells])
            # Fill the A matrix
            for i, p in enumerate(partitions):
                for c in p.cells:
                    A[i][c.gid] = 1 / len(p.cells)
            break

    def solve_qp_with_new_subject(self):
        # TODO: Here we should formulate the problem again but with a new subject which is
        # A(1) * x = u(1)x
        # (This function can be one with the one below "solve_qp".)
        ...

    def solve_qp(self) -> np.array:
        # .T means transponse e.g: [[1, 2], [3, 4]].T => [[1, 3]]
        #                                                 [2, 4]]
        C = .5 * (self.laplacian_matrix + self.laplacian_matrix.T)
        args = [matrix(C), matrix(fixed_pin_x)]
        sol = solvers.qp(*args)
        return np.array(sol['x']).reshape((C.shape[1]))

    def __create_fixed_pin_vectors(self) -> Tuple[np.ndarray, np.ndarray]:
        pin_x_pos, pin_y_pos = [pin.x for pin in self.design.t_nodes], [
            pin.y for pin in self.design.t_nodes]

        # We use "-1 *" just to make it a bit more readable.
        fixed_pin_x = np.array([-1 * np.sum(self.pin_matrix[i] * pin_x_pos[i])
                               for i in range(len(self.design.t_nodes))])
        fixed_pin_y = np.array([-1 * np.sum(self.pin_matrix[i] * pin_y_pos[i])
                               for i in range(len(self.design.t_nodes))])
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
