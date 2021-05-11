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

    def serialize(self):
        return {
            'row_id': self.id,
            'height': self.height,
            'y': self.y,
            'x': self.x,
            'x_end': self.x_end,
            'y_end': self.y_end,
            'cells': [cell.name for cell in self.cells],
            'width': self.width
        }
    # def set_cells(self, cells: List[Node]):
    #     self.cells = cells
