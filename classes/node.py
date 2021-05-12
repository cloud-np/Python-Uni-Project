from typing import Any
import random


class Node:
    def __init__(self, id_: int, name: str, width: int, height: int):
        self.name = name
        self.width = width
        self.height = height
        self.x: Any = None
        self.y: Any = None
        self.id = id_
        random.seed(sum([ord(ch) + 10 for ch in name]))
        self.color = [random.randint(0, 255) for _ in range(3)]
        self.is_terminal: bool = name[0] == 'p'

    def set_position(self, x: int, y: int):
        if self.is_terminal is True and self.x is not None:
            raise Exception(f"You have already set a position for this terminal node!! {self}")
        self.x = x
        self.y = y

    def get_key(self):
        return tuple([self.id, self.name])

    def __key(self):
        return tuple([self.id, self.name])

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        tmp_str = f"Node[{self.id}] {self.name}  w/h: ({self.width},{self.height}) "
        tmp_str += f"pos: ({self.x}, {self.y})" if self.x is not None else ""
        return tmp_str

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

    """Because we need to check only the names we don't want
    to check if they are equal based on id. """
    def __eq__(self, other: "Node"):
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
