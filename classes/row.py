from classes.node import Node
from typing import List, Dict


class PosType:
    START = 0
    CENTER = 1
    END = 2


class Row:
    def __init__(self, id_: int, y: int, x: int, x_end: int, height: int):
        self.id: int = id_
        self.y: int = y
        self.height: float = height
        self.width: float = x_end - x
        self.y_end: int = y + height
        # self.cells: List[Node] = []
        self.x_end: int = x_end
        self.space: float = x_end - x
        self.x: int = x
        self.gap_left: float = x_end - x
        self.avail_x_start: float = x
        self.avail_x_end: float = x_end
        # This is used only from LR Tetris.
        self.cells_pos_added: List[Dict[Node, bool]] = []

    def __str__(self):
        return f"Row[{self.id}] x/y: ({self.x},{self.y})"

    # def get_cells_str(self) -> str:
    #     return "".join(f'{c.name} ' for c in self.cells)

    def get_density(self) -> float:
        return (self.space - self.gap_left) / self.space * 100

    def has_space_for(self, cell):
        return self.gap_left - cell.width >= 0

    # def swap_same_widths_cell(self, old_cell, new_cell):
    #     for c in self.cells_pos_added:
    #         if c['name'] == old_cell.name:
    #             c['name'] = new_cell.name
    #             break
    #     self.cells.remove(old_cell)
    #     self.cells.append(new_cell)

    def add_cell(self, cell, pos_type: PosType = PosType.CENTER) -> None:
        # self.cells.append(cell)
        cell.row = self

        if pos_type == PosType.END:
            self.avail_x_end -= cell.width
            # self.cells_pos_added.append({'name': cell.name, 'pos_type': PosType.END})
        elif pos_type == PosType.START:
            self.avail_x_start += cell.width
            # self.cells_pos_added.append({'name': cell.name, 'pos_type': PosType.START})
        elif pos_type != PosType.CENTER:
            raise ValueError("Uknown PosType given.")
        self.gap_left -= cell.width

    # def get_cell_from_cells_pos(self, cell):
    #     cells_found: List[Node] = [c for c in self.cells_pos_added if c.name == cell.name]
    #     if len(cells_found) != 1:
    #         raise Exception(f"{cell.name} was either not found or two instance and more found in the same row..")
    #     return cells_found[0]['pos_type']

    # def remove_cell(self, cell) -> None:
    #     cell_pos_type = self.get_cell_from_cells_pos(cell)

    #     if cell_pos_type == PosType.END:
    #         self.avail_x_end += cell.width
    #     elif cell_pos_type == PosType.START:
    #         self.avail_x_start -= cell.width

    #     self.gap_left += cell.width
    #     self.cells.remove(cell)
