from colorama import Fore
from typing import List, Iterable
from classes.node import Node


class Net:
    def __init__(self, id_: int, nodes_names: List[str]):
        self.id = id_
        self.nodes_names = nodes_names
        self.nodes: Iterable[Node] = list()
        self.net_degree = len(nodes_names)

    def show_nodes(self):
        tmp_str = "nodes: { "
        for node in self.nodes:
            tmp_str += f"{Fore.GREEN}{node.name}{Fore.RESET}, "
        tmp_str += " }"
        return f"ID: {Fore.MAGENTA}{self.id}{Fore.RESET} {tmp_str}"

    def set_nodes(self, nodes: List[Node]):
        self.nodes = nodes
        self.calc_new_perimeter()

    def calc_new_perimeter(self):
        # min_x = min(self.nodes)
        min_x = min(self.nodes, key=lambda node: node.x)
        min_y = min(self.nodes, key=lambda node: node.y)
        max_x = max(self.nodes, key=lambda node: node.x)
        max_y = max(self.nodes, key=lambda node: node.x)

        # print()

    def serialize(self):
        return {
            'net_id': self.id,
            'nodes_names': self.nodes_names,
            'net_degree': self.net_degree
        }

    def get_key(self):
        return self.id

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other: "Net") -> bool:
        if self.__class__ == other.__class__:
            return self.id == other.id
            # return self.nodes == other.nodes
        else:
            return NotImplemented
