from classes.node import Node
from classes.design import Design
from classes.row import Row
from algos.simulations import simulate_cell_pos
from math import sqrt
from helpers.common_classes import Point
from typing import List, Tuple
from itertools import combinations


class Legalizer:

    def __init__(self, design: Design):
        self.design = design

    def find_collisions(self) -> List[Tuple[Node]]:
        return Legalizer.__find_overlaps(self.design.c_nodes)

    @staticmethod
    def __find_overlaps(cells: List[Node]) -> List[Tuple[Node]]:
        """Check every single pair of nodes for overlaps.
        With the use of the combinations function make every possible combination between
        the nodes and test which of the pairs you made is overlapping each other.

        Parameters
        ----------
        cells : List[Node]
            The cells you want to check for overlapping.

        Returns
        -------
        List[Tuple[Node]]
            A list of the pairs that are overlapping each other.
        """
        return [pair for pair in combinations(cells, 2) if pair[0].rectan.check_overlap(pair[1].rectan)]

    @staticmethod
    def find_dist(p1: Point, p2: Point):
        return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2))

    @staticmethod
    def find_cable_len(design, cell, row):
        @simulate_cell_pos(cell)
        def __find_cable_len(design: Design, cell: Node, row: Row):
            cell.set_position(row.avail_x_start, row.y)
            cable_val: float = design.find_cable_needed()
            return cable_val
        return __find_cable_len(design, cell, row)
