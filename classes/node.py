
class Node:
    def __init__(self, id_: int, name: str, width: int, height: int):
        self.name = name
        self.width = width
        self.height = height
        self.id = id_
        self.is_terminal: bool = name[0] == 'p'

    def get_key(self):
        return tuple([self.id, self.name])

    def __key(self):
        return tuple([self.id, self.name])

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return f"id[{self.id}] {self.name}  w/h: ( {self.width} , {self.height} )"

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
