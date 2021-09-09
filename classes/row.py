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
        self.x_end = x + x_end
        self.x = x
        self.avail_x_start = x

    def __str__(self):
        return f"Row[{self.id}] x/y: ({self.x},{self.y})"

    def has_space_for(self, cell):
        return self.avail_x_start + cell.width < self.x_end

    def add_cell(self, cell):
        self.cells.append(cell)
        self.avail_x_start += cell.width
