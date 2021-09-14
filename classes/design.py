from classes.net import Net
from helpers.dataframes import DataFrameMaker
from classes.node import Node
from classes.row import Row
from typing import List, Set, Iterator


class Design:
    def __init__(self, id_: int, nets: Set[Net], nodes: List[Node], nodes_pos: List[List[str]], rows: List[Row]) -> None:
        self.id = id_
        self.nets: List[Net] = nets
        self.nodes: List[Node] = nodes
        self.rows: List[Row] = rows
        self.width: float = rows[0].width
        self.height: float = sum(r.height for r in rows)
        self.c_nodes = [n for n in nodes if n.is_terminal is False]
        self.t_nodes = [n for n in nodes if n.is_terminal is True]
        self.n_cells = len(self.c_nodes)
        self.n_terminals = len(self.t_nodes)
        self.n_nets = len(self.nets)

        # This has to run first to assign the x and y to each node.
        self.__assign_pos_to_nodes(nodes_pos)
        self.__assign_nodes_to_nets()
        self.__assign_rows_to_cells()

        self.total_area: float = self.width * self.height
        self.total_cell_area: float = sum(n.width * n.height for n in self.nodes)
        self.density: float = (self.total_area - self.total_cell_area) / self.total_area * 100
        self.initial_cable_needed = self.find_cable_needed()

        self.dfm: DataFrameMaker = DataFrameMaker(self)

    def get_dfs(self):
        self.update_dfm()
        return self.dfm.get_dfs()

    def update_dfm(self):
        self.dfm: DataFrameMaker = DataFrameMaker(self)

    def get_nets_in_row_str(self, row) -> str:
        nets = []
        # Keep it like this for readability.
        for c in self.get_cells_in_row(row):
            for net in self.get_nets_containing_node(c):
                if net not in nets:
                    nets.append(net)

        return "".join(str(net.id) + " " for net in nets)

    def get_nets_containing_node_str(self, node) -> str:
        return "".join(
            str(net.id) + " "
            for net in self.get_nets_containing_node(node)
        )

    def change_cells_pos(self, new_xs: List[float], new_ys: List[float]) -> None:
        """Change the pos of all cells.
        This func is getting used from Gordian class mainly.
        Note that when you use this func you should pass the
        same ammount of xs and ys as the cells.
        """
        if len(self.c_nodes) != len(new_xs) or len(self.c_nodes) != len(new_ys):
            raise ValueError(
                "You can't set the positions of some of the cells you need to pas the same len of list for xs and ys")
        [c.set_position(x, y) for c, x, y in zip(self.c_nodes, new_xs, new_ys)]

    def get_cells_in_row(self, row: Row) -> List[Node]:
        cells: List[Node] = [c for c in self.c_nodes if c.row is row]
        # if len(cells) > 1:
        #     raise Exception("Your node can't be in two rows in the same time")
        # elif len(cells) == 0:
        #     return None
        return cells

    def get_nets_containing_node(self, node) -> Iterator:
        # Made it a generator since we gonna iterate it anyway later on.
        return (n for n in self.nets if node in n.nodes)

    def find_node_by_name(self, name: str):
        """Find the a node by a given name.

        It basically makes a generator of nodes that have the given name
        and returns the first one that got found. Or None if none had that name.

        Args:
            name (str): The given name.

        Returns:
            Node | None: Returns either the found node or None.
        """
        found_node = next(
            (node for node in self.nodes if node.name == name), None)
        if found_node is None:
            raise ValueError(f"Could not find a node by name: {name}")
        return found_node

    def __assign_rows_to_cells(self):
        """Assign the nodes to the correct rows.

        e.g:
        Node(y=170)
        (y - 100) // 10 = 7
        Which is the 8th row so we can do:
        cell = rows[7]
        """
        for cell in self.c_nodes:
            cell = self.rows[(cell.y - 100) // 10]

    def __assign_nodes_to_nets(self):
        for net in self.nets:
            net.set_nodes([self.find_node_by_name(n_name)
                          for n_name in net.nodes_names])

    def __assign_pos_to_nodes(self, pos: List[List[str]]) -> None:
        [self.find_node_by_name(name=arr[0]).set_position(
            int(arr[1]), int(arr[2])) for arr in pos]

    def find_cable_needed(self):
        return sum(net.calc_new_perimeter() for net in self.nets)
