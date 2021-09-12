from classes.design import Design
import pandas as pd
from classes.row import Row
from typing import List


columns_for_rows = ["id", "density", "cells", "nets", "x", "y"]
columns_for_design = ["density", "n_cells", "n_terminals", "n_nets", "width", "height", "total_area", "total_cell_area"]
columns_for_nodes = ["name", "width", "height", "x", "y", "n-row", "nets", "is_terminal"]
columns_for_nets = ["id", "nodes", "semiperimeter"]


class DataFrameMaker:
    def __init__(self, design: Design):
        self.nodes_df = DataFrameMaker.for_nodes(design)
        self.nets_df = DataFrameMaker.for_nets(design)
        self.design_df = DataFrameMaker.for_design(design)
        self.rows_df = DataFrameMaker.for_rows(design)
        # Filter all terminal nodes out.
        self.cell_df = self.nodes_df.loc[self.nodes_df['name'].str[0] != 'p']
        print(self.cell_df['width'].argmin())
        print(self.cell_df['width'].argmax())
        print(self.cell_df['width'].mean())

        print(self.rows_df)
        print(self.rows_df['density'].argmin())
        print(self.rows_df['density'].argmax())
        print(self.rows_df['density'].mean())

    @staticmethod
    def for_nets(design: Design) -> pd.DataFrame:
        nodes_dict = {col: [] for col in columns_for_nets}
        for nt in design.nets:
            for col in columns_for_nets:
                if col == 'nodes':
                    nodes_dict[col].append(nt.get_nodes_str())
                else:
                    nodes_dict[col].append(getattr(nt, col))

        return pd.DataFrame(nodes_dict)

    @staticmethod
    def for_design(design: Design) -> pd.DataFrame:
        nodes_dict = {col: [] for col in columns_for_design}
        for col in columns_for_design:
            nodes_dict[col].append(getattr(design, col))

        return pd.DataFrame(nodes_dict)

    @staticmethod
    def for_rows(design: Design) -> pd.DataFrame:
        nodes_dict = {col: [] for col in columns_for_rows}
        for r in design.rows:
            for col in columns_for_rows:
                if col == 'cells':
                    nodes_dict[col].append(r.get_cells_str())
                elif col == 'density':
                    nodes_dict[col].append(r.get_density())
                elif col == 'nets':
                    nodes_dict[col].append(design.get_nets_in_row_str(r))
                else:
                    nodes_dict[col].append(getattr(r, col))

        return pd.DataFrame(nodes_dict)

    @staticmethod
    def for_nodes(design) -> pd.DataFrame:
        nodes_dict = {col: [] for col in columns_for_nodes}
        for n in design.nodes:
            for col in columns_for_nodes:
                if col == 'n-row':
                    nodes_dict[col].append(format_row_num_for_node_df(design.get_row_containing_node(n)))
                elif col == 'nets':
                    nodes_dict[col].append(design.get_nets_containing_node_str(n))
                else:
                    nodes_dict[col].append(getattr(n, col))
        return pd.DataFrame(nodes_dict)


def format_row_num_for_node_df(rows: List[Row]):
    if not rows:
        return '-'
    return f'{rows[0].id}'
