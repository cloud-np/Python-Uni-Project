from colorama import Fore
from typing import List
from classes.node import Node


class Net:
    def __init__(self, id_: int, nodes_names: List[str]):
        self.id = id_
        self.nodes_names = nodes_names
        self.nodes: List[Node] = list()
        self.net_degree = len(nodes_names)
        self.semiperimeter: int = -1

    def show_nodes(self):
        tmp_str = "nodes: { "
        for node in self.nodes:
            tmp_str += f"{Fore.GREEN}{node.name}{Fore.RESET}, "
        tmp_str += " }"
        return f"ID: {Fore.MAGENTA}{self.id}{Fore.RESET} {tmp_str}\n"

    def set_nodes(self, nodes: List[Node]):
        self.nodes = nodes
        self.calc_new_perimeter()

    def calc_new_perimeter(self):
        # min_x = min(self.nodes)
        min_x = min(self.nodes, key=lambda node: node.x).x
        min_y = min(self.nodes, key=lambda node: node.y).y
        max_x = max(self.nodes, key=lambda node: node.x).x
        max_y = max(self.nodes, key=lambda node: node.y).y
        # semiPerimeterSum += Math.abs(maxX - minX) + Math.abs(maxY - minY);
        self.semiperimeter = abs(max_x - min_x) + abs(max_y - min_y)

        # print()

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
