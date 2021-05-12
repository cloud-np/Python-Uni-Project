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

    def __str__(self):
        return f"Row[{self.id}] x/y: ({self.x},{self.y})"
    # def set_cells(self, cells: List[Node]):
    #     self.cells = cells
