from typing import Set
from classes.net import Net
from classes.node import Node
from typing import List


class Design:
    def __init__(self, id_: int, num_pins: int, nets: Set[Net], nodes: Set[Node]) -> None:
        self.id = id_
        self.num_pins = num_pins
        self.nets = nets
        self.nodes = nodes

    def find_node_by_name(self, name: str):
        return next((node for node in self.nodes if node.name == name), None)

    def assign_pos_to_nodes(self, pos: List[List[str]]) -> None:
        for arr in pos:
            found_node = self.find_node_by_name(name=arr[0])
            if found_node is None:
                raise ValueError(f"Could not find a node by name: {arr[0]}")
            found_node.set_position(int(arr[1]), int(arr[2]))
