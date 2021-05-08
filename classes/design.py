from classes.net import Net
from classes.node import Node
from classes.row import Row
from typing import List, Set


class Design:
    def __init__(self, id_: int, num_pins: int, nets: Set[Net], nodes: List[Node], rows: List[Row]) -> None:
        self.id = id_
        self.num_pins = num_pins
        self.nets = nets
        self.nodes = nodes
        self.c_nodes = [n for n in nodes if n.is_terminal is False]
        self.t_nodes = [n for n in nodes if n.is_terminal is True]

        self.assign_nodes_to_nets()

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

    def assign_nodes_to_nets(self):
        [net.nodes.append(self.find_node_by_name(n_name)) for net in self.nets for n_name in net.nodes_names]

    def assign_pos_to_nodes(self, pos: List[List[str]]) -> None:
        [self.find_node_by_name(name=arr[0]).set_position(int(arr[1]), int(arr[2])) for arr in pos]
