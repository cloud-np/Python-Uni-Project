from classes.node import Node


class Parser:
    def __init__(
        self,
        path_to_nets: str = "./data/design.nets",
        path_to_nodes: str = "./data/design.nodes",
        path_to_pl: str = "./data/design.pl",
        path_to_scl: str = "./data/design.scl",
    ):
        self.path_to_nets = path_to_nets
        self.path_to_nodes = path_to_nodes
        self.path_to_pl = path_to_pl
        self.path_to_scl = path_to_scl

    def parse_nodes(self):
        # Make list here with size of len(nodes)
        nodes_list: list[Node] = []
        with open(self.path_to_nodes, "r") as nodes_file:
            nodes_lines = nodes_file.readlines()[7:]

            for i, line in enumerate(nodes_lines):
                line_splited = line.split()
                nodes_list.append(
                    Node(i, line_splited[0], int(line_splited[1]), int(line_splited[2]))
                )
        return nodes_list