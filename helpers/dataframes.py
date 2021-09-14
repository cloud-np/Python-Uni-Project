import pandas as pd
from classes.row import Row


columns_for_rows = ["id", "density", "cells", "nets", "x", "y"]
columns_for_design = ["density", "n_cells", "n_terminals", "n_nets", "width", "height", "total_area", "total_cell_area"]
columns_for_nodes = ["name", "width", "height", "x", "y", "n-row", "nets", "is_terminal"]
columns_for_nets = ["id", "nodes", "semiperimeter"]


class DataFrameMaker:
    def __init__(self, design):
        self.design = design
        self.nodes_df = DataFrameMaker.for_nodes(design)
        self.nets_df = DataFrameMaker.for_nets(design)
        self.design_df = DataFrameMaker.for_design(design)
        self.rows_df = DataFrameMaker.for_rows(design)
        # Filter all terminal nodes out.
        self.cell_df = self.nodes_df.loc[self.nodes_df['name'].str[0] != 'p']
        self.cell_df.set_index('name', inplace=True)

    def get_dfs(self):
        return self.design_df, self.rows_df, self.nodes_df, self.nets_df

    def __str__(self) -> str:
        print("NOTE shows the rows id")
        print("Cell with smallest width: ", self.cell_df['width'].argmin())
        print("Cell with biggest width: ", self.cell_df['width'].argmax())
        print("Avg Cell width: ", self.cell_df['width'].mean())
        print("Row with lowest density: ", self.rows_df['density'].argmin())
        print("Row with highest density: ", self.rows_df['density'].argmax())
        print("Avg Row density: ", self.rows_df['density'].mean())
        print("Half Perim: ", self.design.find_cable_needed())
        print("Design density: ", self.design_df['density'].argmin())
        nets_info = self.get_nets_info()
        print("Smallest net: ", nets_info[0])
        print("Biggest net: ", nets_info[1])
        return ''

    @staticmethod
    def for_nets(design) -> pd.DataFrame:
        nodes_dict = {col: [] for col in columns_for_nets}
        for nt in design.nets:
            for col in columns_for_nets:
                if col == 'nodes':
                    nodes_dict[col].append(nt.get_nodes_str())
                else:
                    nodes_dict[col].append(getattr(nt, col))

        return pd.DataFrame(nodes_dict)

    @staticmethod
    def for_design(design) -> pd.DataFrame:
        nodes_dict = {col: [] for col in columns_for_design}
        for col in columns_for_design:
            nodes_dict[col].append(getattr(design, col))

        return pd.DataFrame(nodes_dict)

    def get_nets_info(self):
        return min(self.design.nets, key=lambda n: len(n.nodes)).id, max(self.design.nets, key=lambda n: len(n.nodes)).id

    @staticmethod
    def for_rows(design) -> pd.DataFrame:
        nodes_dict = {col: [] for col in columns_for_rows}
        for r in design.rows:
            for col in columns_for_rows:
                if col == 'cells':
                    nodes_dict[col].append("".join(c.name + " " for c in design.get_cells_in_row(r)))
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
                    nodes_dict[col].append(format_row_num_for_node_df(n.row))
                elif col == 'nets':
                    nodes_dict[col].append(design.get_nets_containing_node_str(n))
                else:
                    nodes_dict[col].append(getattr(n, col))
        return pd.DataFrame(nodes_dict)


def format_row_num_for_node_df(row: Row):
    if row is None:
        return '-'
    return f'{row.id}'
