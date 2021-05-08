from colorama import Fore


class Net:
    def __init__(self, id_, nodes: set):
        self.id = id_
        self.nodes: set = nodes
        self.net_degree = len(nodes)

    def __str__(self):
        tmp_str = "nodes: { "
        for node in self.nodes:
            tmp_str += f"{Fore.GREEN}{node.name}{Fore.RESET}, "
        tmp_str += " }"
        return f"ID: {Fore.MAGENTA}{self.id}{Fore.RESET} {tmp_str}"

    def __eq__(self, other):
        if isinstance(other, Net):
            return self.id == other.id
            # return self.nodes == other.nodes
        else:
            return NotImplemented
