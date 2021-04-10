class Node:
    def __init__(self, id_, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.id = id_
        self.is_terminal = name[0] == 'p'

    def get_key(self):
        return tuple([self.id, self.name])

    def __key(self):
        return tuple([self.id, self.name])

    def __hash__(self):
        return hash(self.__key())

    """Because we need to check only the names we don't want
    to check if they are equal based on id. """
    def __eq__(self, other):
        if isinstance(other, Node):
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