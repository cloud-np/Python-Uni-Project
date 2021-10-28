from classes.design import Design
from classes.node import Node
from algos.legalizer import Legalizer
from algos.simulations import simulate_many_cells_pos
from typing import Iterator, T, List


class SwapType:
    FIRST_FIT = 0
    BEST_FIT = 1


# NOTE I should make a class that helps me iterate the cells
# because I wrote similar stuff for Tetris class and they
# could just extend that class refactor this later.
class Swapper:
    def __init__(self, design: Design, variant: int, is_checking: bool):
        self.design: Design = design
        self.variant: int = variant
        self.counter_cell_pos: int = 0
        self.n_cells: int = len(self.design.c_nodes)
        self.last_cell: Node = None
        self.first_iter: bool = False
        self.is_checking: bool = is_checking
        if is_checking:
            self.legalizer = Legalizer(design)
        self.ended: bool = False

    def sim_swap_two_cells(self, cell, cell2):
        @simulate_many_cells_pos(cell, cell2)
        def __sim_swap_two_cell(cell, cell2):
            Swapper.swap_two_cells(cell, cell2)
            return self.design.find_cable_needed()
        return __sim_swap_two_cell(cell, cell2)

    @staticmethod
    def swap_two_cells(cell, cell2):
        c1_pos = (cell.x, cell.y)

        cell.set_position(cell2.x, cell2.y)
        cell2.set_position(*c1_pos)

    def find_best_swappable_cell(self, cell):
        before_swap_val: float = self.design.find_cable_needed()
        swappables_info: List[dict] = [{'val': self.sim_swap_two_cells(cell, c), 'c1': cell, 'c2': c} for c in self.find_same_width_cells(cell)]

        if not swappables_info:
            return None
        best_swap = min(swappables_info, key=lambda swi: swi['val'])
        # If the swap we do is not better than what
        # we had initially then simple do not do it.
        if best_swap['val'] < before_swap_val:
            return best_swap
        return None

    def has_ended(self):
        return self.ended

    def get_curr_cell(self):
        if self.counter_cell_pos >= self.n_cells:
            return None
        return self.design.c_nodes[self.counter_cell_pos]

    def get_last_cell(self):
        if self.counter_cell_pos == 0:
            return None
        return self.design.c_nodes[self.counter_cell_pos - 1]

    def run(self) -> 'Swapper':
        for _ in range(self.n_cells):
            self.next()
        return self

    def next(self):
        if self.has_ended():
            return None

        if self.variant == SwapType.FIRST_FIT:
            cell = self.design.c_nodes[self.counter_cell_pos]
            best_swap = self.find_best_swappable_cell(cell)
            if best_swap is None:
                self.counter_cell_pos += 1
                if self.counter_cell_pos >= self.n_cells:
                    self.ended = True
            else:
                Swapper.swap_two_cells(best_swap['c1'], best_swap['c2'])
                self.counter_cell_pos = 0
        elif self.variant == SwapType.BEST_FIT:
            all_best_swaps = [self.find_best_swappable_cell(c) for c in self.design.c_nodes]
            all_best_swaps = list(filter(None, all_best_swaps))

            if not all_best_swaps:
                self.ended = True
            else:
                best_swap = min(all_best_swaps, key=lambda bs: bs['val'])
                Swapper.swap_two_cells(best_swap['c1'], best_swap['c2'])

        if self.is_checking:
            cols = self.legalizer.find_collisions()
            if len(cols) > 0:
                raise Exception('Collisions found after swap!')

    def find_same_width_cells(self, cell) -> Iterator[T]:
        return filter(lambda c: (c.width == cell.width) and (c is not cell), self.design.c_nodes)
