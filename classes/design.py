from classes.net import Net
from classes.node import Node
from classes.row import Row
from typing import List, Set


class Design:
    def __init__(self, id_: int, nets: Set[Net], nodes: List[Node], nodes_pos: List[List[str]], rows: List[Row]) -> None:
        self.id = id_
        self.nets = nets
        self.nodes = nodes
        self.rows = rows
        self.c_nodes = [n for n in nodes if n.is_terminal is False]
        self.t_nodes = [n for n in nodes if n.is_terminal is True]

        # This has to run first to assign the x and y to each node.
        self.assign_pos_to_nodes(nodes_pos)
        self.assign_nodes_to_nets()
        self.assign_nodes_to_rows()

        self.initial_cable_needed = self.find_cable_needed()

    def change_cells_pos(self, new_xs, new_ys):
        [c.set_position(x, y) for c, x, y in zip(self.c_nodes, new_xs, new_ys)]

    def find_node_by_name(self, name: str):
        """Find the a node by a given name.

        It basically makes a generator of nodes that have the given name
        and returns the first one that got found. Or None if none had that name.

        Args:
            name (str): The given name.

        Returns:
            Node | None: Returns either the found node or None.
        """
        found_node = next((node for node in self.nodes if node.name == name), None)
        if found_node is None:
            raise ValueError(f"Could not find a node by name: {name}")
        return found_node

    def assign_nodes_to_rows(self):
        """Assign the nodes to the correct rows.

        e.g:
        Node(y=170)
        (y - 100) // 10 = 7
        Which is the 8th row so we can do:
        rows[7].cells.append(node)
        """
        for cell in self.c_nodes:
            self.rows[(cell.y - 100) // 10].cells.append(cell)

    def assign_nodes_to_nets(self):
        for net in self.nets:
            net.set_nodes([self.find_node_by_name(n_name) for n_name in net.nodes_names])

    def assign_pos_to_nodes(self, pos: List[List[str]]) -> None:
        [self.find_node_by_name(name=arr[0]).set_position(int(arr[1]), int(arr[2])) for arr in pos]

    def find_cable_needed(self):
        return sum(net.calc_new_perimeter() for net in self.nets)
