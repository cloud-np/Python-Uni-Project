from classes.node import Node
from typing import List


class Row:
    def __init__(self, id_: int, y: int, x: int, x_end: int, height: int):
        self.id = id_
        self.y = y
        self.height = height
        self.width = x_end - x
        self.y_end = y + height
        self.cells: List[Node] = []
        self.x_end = x_end
        self.x = x
        self.gap_left: float = x_end - x
        self.avail_x_start: float = x
        self.avail_x_end: float = x_end

    def __str__(self):
        return f"Row[{self.id}] x/y: ({self.x},{self.y})"

    def has_space_for(self, cell):
        return self.gap_left - cell.width >= 0

    def swap_cell(self):
        ...

    def add_cell(self, cell, add_to_end: bool = False):
        self.cells.append(cell)

        if add_to_end:
            self.avail_x_end -= cell.width
        else:
            self.avail_x_start += cell.width
        self.gap_left -= cell.width
