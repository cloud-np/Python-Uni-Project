from typing import Set
from classes.net import Net
from classes.node import Node


class Desgin:
    def __init__(self, id_: int, num_pins: int, nets: Set[Net], nodes: Set[Node]) -> None:
        self.id = id_
        self.num_pins = num_pins
        self.nets = nets
        self.nodes = nodes
