from typing import Union, Tuple
import pandas as pd
from helpers.common_classes import Rectangular
# from classes.row import Row
import random


class Node:
    def __init__(self, id_: int, gid: int, name: str, width: int, height: int):
        self.name: str = name
        self.width: float = width
        self.height: float = height
        self.x: Union[int, None] = None
        self.y: Union[int, None] = None
        self.rectan: Union[Rectangular, None] = None
        # "gid" is basically group-id which means the following:
        # p1.gid = 0
        # p2.gid = 1
        # a1.gid = 0
        # a3.gid = 2
        # etc
        # Nodes from different groups can have the same gid!!
        # but there is one unique "id" for every Node!!
        self.gid: int = gid
        self.id: int = id_
        random.seed(sum(ord(ch) + 10 for ch in name))
        self.color: Tuple[int] = [random.randint(0, 255) for _ in range(3)]
        self.og_color: Tuple[int] = self.color
        self.is_terminal: bool = name[0] == 'p'
        self.row = None
        self.df = None

    def set_position(self, x: int, y: int) -> None:
        if self.is_terminal is True and self.x is not None:
            raise Exception(f"You have already set a position for this terminal node!! {self}")
        self.x = x
        self.y = y
        self.rectan = Rectangular(x, y, self.width, self.height)
        self.update_df()

    def update_df(self) -> None:
        if self.df is not None:
            self.df.update({'x': self.x, 'y': self.y})

    def get_key(self):
        return tuple([self.gid, self.name])

    def __key(self):
        return tuple([self.gid, self.name])

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        tmp_str = f"Node[{self.gid}] {self.name}  w/h: ({self.width},{self.height}) "
        tmp_str += f"pos: ({self.x}, {self.y})" if self.x is not None else ""
        return tmp_str + '\n'

    def __lt__(self, other: "Node"):
        if self.__class__ == other.__class__:
            return self.name < other.name
        else:
            return NotImplemented

    def __gt__(self, other: "Node"):
        if self.__class__ == other.__class__:
            return self.name > other.name
        else:
            return NotImplemented

    def __eq__(self, other: "Node"):
        """Because we need to check only the names we don't want to check if they are equal based on id. """
        if self.__class__ == other.__class__:
            return self.name == other.name
            # return self.__key() == other.__key()
        else:
            return NotImplemented

    # def __lt__(self, other):
    #     if isinstance(other, Node):
    #         return self.id < other.id
    #     else:
    #         return NotImplemented

    # def __gt__(self, other):
    #     if isinstance(other, Node):
    #         return self.id > other.id
    #     else:
    #         return NotImplemented
