from classes.node import Node
from helpers.project_parser import Parser
from typing import List
from classes.design import Design
from helpers.common_classes import Point
from algos.legalizer import Legalizer


class Tetris:
    def __init__(self, design: Design, lower_cable_usage: bool = False, left_right: bool = False):
        self.design: Design = design
        self.counter_cell_pos: int = 0
        self.last_cell: Node = None
        self.left_right: bool = left_right
        self.is_place_right: bool = False
        self.lower_cable_usage = lower_cable_usage
        self.n_cells: int = len(self.design.c_nodes)
        self.first_iter: bool = False

    def __calc_best_cable_for_cell(self, cell):
        # If our row has space for our cell then it will try
        # to simulate putting that cell there and finding
        # the new cable len that is needed for the design.
        cables = [{'val': Legalizer.find_cable_len(self.design, cell, r), 'row': r} for r in self.design.rows if r.has_space_for(cell)]
        self.pick_best_row_for_cell(cables, cell)

    def get_variant_name(self):
        if self.left_right:
            return 'Left-Right Tetris'
        elif self.lower_cable_usage:
            return 'Lower cable usage Tetris'
        else:
            return 'Vanilla Tetris'

    def run(self) -> 'Tetris':
        for _ in range(self.n_cells):
            self.next()
        return self

    @staticmethod
    def run_every_tetris_variant() -> List[dict]:
        run_info: List[dict] = []
        for variant in [(False, False), (True, False), (False, True)]:
            parser = Parser(design_path='./data/')
            design: Design = parser.parse_design()
            t = Tetris(design, *variant).run()
            run_info.append({'name': t.get_variant_name(), 'cable_len': design.find_cable_needed()})
        return run_info

    def pick_best_row_for_cell(self, dict_rows: dict, cell: Node):
        min_row = min(dict_rows, key=lambda cab: cab['val'])

        if self.is_place_right:
            x = min_row['row'].avail_x_end - cell.width
            min_row['row'].add_cell(cell, add_to_end=True)
        else:
            x = min_row['row'].avail_x_start
            min_row['row'].add_cell(cell)

        cell.set_position(x, min_row['row'].y)

    def __calc_best_dist_for_cell_lr(self, cell: Node):
        # If our row has space for our cell then it will try to find the distance it needs to that position.
        dists = []
        for r in self.design.rows:
            if r.has_space_for(cell):
                row_x = r.avail_x_end - cell.width if self.is_place_right else r.avail_x_start
                dists.append({'val': Legalizer.find_dist(Point(cell.x, cell.y), Point(row_x, r.y)), 'row': r})

        self.pick_best_row_for_cell(dists, cell)

    def __calc_best_dist_for_cell(self, cell):
        # If our row has space for our cell then it will try to find the distance it needs to that position.
        dists = [{'val': Legalizer.find_dist(Point(cell.x, cell.y), Point(r.avail_x_start, r.y)), 'row': r} for r in self.design.rows if r.has_space_for(cell)]
        self.pick_best_row_for_cell(dists, cell)

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
        if self.has_ended():
            return None
        cell = self.design.c_nodes[self.counter_cell_pos]

        # Pick the legalization way basically.
        if self.lower_cable_usage:
            self.__calc_best_cable_for_cell(cell)
        elif self.left_right:
            if self.first_iter is False:
                sorted(self.design.c_nodes, key=lambda c: c.x)
            # This start picks cells from the end of our sorted list
            # (our list is sorted once we made the Tetris obj)
            if self.is_place_right:
                cell = self.design.c_nodes[self.n_cells - self.counter_cell_pos]
            self.__calc_best_dist_for_cell_lr(cell)
            # Its False to begin with because we want
            # to place the first cell Left then Right etc.
            self.is_place_right = not self.is_place_right
        else:
            self.__calc_best_dist_for_cell(cell)

        self.counter_cell_pos += 1
        return cell
