from classes.design import Design
from colorama import Fore
from classes.node import Node
import numpy as np
from cvxopt import matrix, solvers
from data.gordian_example import eg_cell_matrix, eg_pin_matrix, eg_fixed_pin_x, eg_fixed_pin_y
from typing import List, Tuple


# NOTE: Maybe change border points to x, x_end and
# y, y_end. More readable/easier to work with plus
# more  consistent with what you wrote in Node class
class Partition:
    def __init__(self, _id: int, cells: List[Node], border_xs: np.array, border_ys: np.array, cut_point: float) -> None:
        self.id: int = _id
        self.cells: List[Node] = cells
        self.border_xs: np.array = border_xs
        self.border_ys: np.array = border_ys
        self.cut_point: float = cut_point
        self.center: np.array = np.array(
            [(self.border_xs[0] + self.border_xs[1]) / 2, (self.border_ys[0] + self.border_ys[1]) / 2])

    def __len__(self) -> int:
        return len(self.cells)

    def get_upper_cells_bound(self, for_x: bool) -> np.array:
        border_val: float = self.border_xs[1] if for_x else self.border_ys[1]
        return np.array(len(self.cells) * [border_val])

    @staticmethod
    def create_initial_partitions(cells, rows) -> Tuple['Partition']:
        # We sort by the x attr
        sorted_cells: List[Node] = sorted(cells, key=lambda c: c.x)
        sc_half: int = len(sorted_cells) // 2
        f_half_c: List[Node] = sorted_cells[:sc_half]
        s_half_c: List[Node] = sorted_cells[sc_half:]
        # We initially make the cut in the Y axis.
        border_xs, border_xs2 = Partition.__create_subparts_borders(rows[0].x, rows[len(rows) - 1].x_end)
        return Partition(0, cells=f_half_c, border_xs=border_xs, border_ys=np.array((0, 800)), cut_point=border_xs[1]), Partition(1, cells=s_half_c, border_xs=border_xs2, border_ys=np.array((0, 800)), cut_point=border_xs[1])

    @staticmethod
    def get_uxys_from_parts(partitions: List['Partition']) -> Tuple[List[int]]:
        ux = [p.center[0] for p in partitions]
        uy = [p.center[1] for p in partitions]
        return ux, uy

    def get_cut_point(self):
        return len(self.cells) * [self.cut_point]

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
            borders_y = self.border_ys
            borders_y2 = self.border_ys
            borders_x, borders_x2 = Partition.__create_subparts_borders(*self.border_xs)
            cut_point: float = borders_x[1]
        else:
            borders_x = self.border_xs
            borders_x2 = self.border_xs
            borders_y, borders_y2 = Partition.__create_subparts_borders(*self.border_ys)
            cut_point: float = borders_y[1]

        cells = Partition.find_cells_in_area(partition=self, cells=self.cells, area=(borders_x, borders_y))
        cells2 = Partition.find_cells_in_area(partition=self, cells=self.cells, area=(borders_x2, borders_y2))
        return Partition(self.id + 1, cells=cells, border_xs=borders_x, border_ys=borders_y, cut_point=cut_point), Partition(self.id + 2, cells=cells2, border_xs=borders_x2, border_ys=borders_y2, cut_point=cut_point)


class Gordian:
    def __init__(self, design: Design, load_example: bool = False):
        self.load_example = load_example
        if not load_example:
            self.design: Design = design
            num_cnodes: int = len(self.design.c_nodes)

            self.pin_matrix: np.ndarray = np.zeros(
                (num_cnodes, len(self.design.t_nodes)))
            self.cell_matrix: np.ndarray = np.zeros((num_cnodes, num_cnodes))
            self.__populate_cell_and_pin_matrixs()

            self.fixed_pin_x, self.fixed_pin_y = self.__create_fixed_pin_vectors()
        else:
            self.pin_matrix, self.cell_matrix = eg_pin_matrix, eg_cell_matrix
            self.fixed_pin_x, self.fixed_pin_y = eg_fixed_pin_x, eg_fixed_pin_y
        self.degree_matrix: np.ndarray = self.__create_degree_matrix()
        self.laplacian_matrix: np.ndarray = self.degree_matrix - self.cell_matrix

    @staticmethod
    def find_middle_point(xs: Tuple[float], ys: Tuple[float]) -> Tuple[float]:
        return ([(xs[0] + xs[1]) / 2, (ys[0] + ys[1]) / 2])

    def stopping_cond_met(self, partitions: List[Node]) -> bool:
        return any(len(p) < 2 for p in partitions)

    @staticmethod
    def __print_qp_output(level: int, cells_pos):
        print(f"{level} QP formulation.")
        print(f"x positions of cells: \n{Fore.GREEN}{cells_pos[0]}{Fore.RESET}\ny positions of cells: \n{Fore.MAGENTA}{cells_pos[1]}{Fore.RESET}")

    def run_example(self):
        cells_xs: List[float] = self.solve_qp(is_x=True)
        cells_ys: List[float] = self.solve_qp(is_x=False)
        Gordian.__print_qp_output(0, (cells_xs, cells_ys))

        A = [[1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5]]
        A = np.array(A)
        ux, uy = [1., 3.], [2., 2.]
        cells_xs: List[float] = self.solve_qp(is_x=True, A=A, u=ux)
        cells_ys: List[float] = self.solve_qp(is_x=False, A=A, u=uy)
        Gordian.__print_qp_output(1, (cells_xs, cells_ys))

        A = [[0, 0, 1 / 2, 1 / 2, 0, 0, 0, 0, 0, 0],
             [1 / 3, 1 / 3, 0, 0, 1 / 3, 0, 0, 0, 0, 0],
             [0, 0, 1 / 2, 1 / 2, 0, 0, 1 / 2, 0, 0, 1 / 2],
             [0, 0, 0, 0, 0, 1 / 3, 0, 1 / 3, 1 / 3, 0]]
        A = np.array(A)
        ux, uy = [1., 1., 3., 3.], [3.2, 1.2, 3.2, 1.2]
        cells_xs: List[float] = self.solve_qp(is_x=True, A=A, u=ux)
        cells_ys: List[float] = self.solve_qp(is_x=False, A=A, u=uy)
        Gordian.__print_qp_output(2, (cells_xs, cells_ys))

    def run(self) -> None:

        # If the example was loaded run the example instead
        if self.load_example:
            self.run_example()
            return

        # 0 QP Formulation
        partitions = Partition.create_initial_partitions(
            self.design.c_nodes, self.design.rows)
        n_cells = len(self.design.c_nodes)
        cells_xs: List[float] = self.solve_qp(is_x=True)
        cells_ys: List[float] = self.solve_qp(is_x=False)
        self.design.change_cells_pos(cells_xs, cells_ys)

        # 1 QP Formulation
        # At first the A matrix has only 2 rows since our partitions are only 2.
        A: np.ndarray = np.zeros((2, n_cells))
        A[0][:len(partitions[0])] = 1 / len(partitions[0])
        A[1][len(partitions[1]):] = 1 / len(partitions[1])
        # ux and uy from the centers from the partitions
        ux: np.array = np.array(
            [partitions[0].center[0], partitions[1].center[0]])
        uy: np.array = np.array(
            [partitions[0].center[1], partitions[1].center[1]])

        # n QP Formulation
        seperate_on_y = False
        while not self.stopping_cond_met(partitions):
            self.solve_qp_and_set_cells_pos(partitions, A, ux, uy)
            # Get new subpartitions from current partitions
            partitions: List[Tuple[Partition]] = [p.create_sub_partitions(seperate_on_y) for p in partitions]

            # This is done to unpack the tuples inside the list because each
            # partitions gives us back a tuple of two subsparts. This operation
            # is called 'flatten' in other languages.
            partitions = sum(partitions, ())
            seperate_on_y = not seperate_on_y
            # Get the centers from the Partitions.
            ux, uy = Partition.get_uxys_from_parts(partitions)
            # Create the A matrix. The number of rows
            # depends from how many partitions we have
            A: np.ndarray = np.zeros([len(partitions), n_cells])
            for i, p in enumerate(partitions):
                for c in p.cells:
                    A[i][c.gid] = 1 / len(p.cells)

    def solve_qp_and_set_cells_pos(self, partitions, A, ux, uy):

        G: np.ndarray = np.zeros([len(self.design.c_nodes), len(self.design.c_nodes)])
        upper_bounds = [p.get_upper_cells_bound(for_x=True) for p in partitions]
        np.fill_diagonal(G, upper_bounds)
        h = [p.get_cut_point() for p in partitions]
        h = sum(h, [])

        cells_xs: List[float] = self.solve_qp(is_x=True, G=G, h=h, A=A, u=ux)
        cells_ys: List[float] = self.solve_qp(is_x=False, G=G, h=h, A=A, u=uy)
        self.design.change_cells_pos(cells_xs, cells_ys)

    def solve_qp(self, is_x: bool, G=None, h=None, A=None, u=None) -> np.array:
        # .T means transponse e.g: [[1, 2], [3, 4]].T => [[1, 3]]
        #                                                 [2, 4]]
        C = .5 * (self.laplacian_matrix + self.laplacian_matrix.T)

        if A is None:
            sol = solvers.qp(P=matrix(C), q=matrix(self.fixed_pin_x))
        elif self.load_example:
            sol = solvers.qp(P=matrix(C), q=matrix(self.fixed_pin_x), A=matrix(A), b=matrix(u))
        else:
            sol = solvers.qp(P=matrix(C), q=matrix(self.fixed_pin_x), G=matrix(G), h=matrix(h), A=matrix(A), b=matrix(u))
        return np.array(sol['x']).reshape((C.shape[1]))

    def __create_fixed_pin_vectors(self) -> Tuple[np.ndarray, np.ndarray]:
        pin_x_pos, pin_y_pos = [pin.x for pin in self.design.t_nodes], [
            pin.y for pin in self.design.t_nodes]

        return self.__create_fixed_pin_vector(pin_x_pos), self.__create_fixed_pin_vector(pin_y_pos)

    def __create_fixed_pin_vector(self, pin_vector: List[float]):
        return np.array([
            -1 * sum(self.pin_matrix[i][j] * pin_vector[j]
                     for j in range(len(self.design.t_nodes)))
            for i in range(len(self.design.c_nodes))
        ])

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
