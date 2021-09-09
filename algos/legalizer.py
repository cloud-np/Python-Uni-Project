from classes.node import Node
from classes.design import Design
from math import sqrt
from helpers.common_classes import Point
from typing import List, Tuple
from itertools import combinations


class Legalizer:

    def __init__(self, design: Design):
        self.design = design
        collisions = Legalizer.__check_for_overlaps(self.design.c_nodes)
        if len(collisions) > 0:
            for c in collisions:
                for a in c:
                    print(a)
        else:
            print('No collisions found!')

    def __check_for_overlaps(cells: List[Node]) -> List[Tuple[Node]]:
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


class Tetris:
    def __init__(self, design: Design):
        self.design: Design = design
        self.counter_cell_pos: int = 0
        self.last_cell: Node = None
        self.n_cells: int = len(self.design.c_nodes)

    def __calc_best_dist_for_cell(self, cell):
        # If our row has space for our cell then it will try to find the distance it needs to that position.
        dists = [{'dist': Legalizer.find_dist(Point(cell.x, cell.y), Point(r.avail_x_start, r.y)), 'row': r} for r in self.design.rows if r.has_space_for(cell)]
        min_row = min(dists, key=lambda d: d['dist'])
        cell.set_position(min_row['row'].avail_x_start, min_row['row'].y)
        min_row['row'].add_cell(cell)

    def has_ended(self):
        return self.counter_cell_pos >= self.n_cells

    def get_curr_cell(self):
        if self.counter_cell_pos >= self.n_cells:
            return None
        return self.design.c_nodes[self.counter_cell_pos]

    def get_last_cell(self):
        if self.counter_cell_pos == 0:
            return None
        return self.design.c_nodes[self.counter_cell_pos - 1]

    def next(self):
        if self.counter_cell_pos >= self.n_cells:
            return None
            # raise StopIteration()
        cell = self.design.c_nodes[self.counter_cell_pos]
        self.__calc_best_dist_for_cell(cell)
        self.counter_cell_pos += 1
        return cell
