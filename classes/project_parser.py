from classes.node import Node
from classes.net import Net
from classes.row import Row
from typing import List


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

            for line in nodes_lines:
                line_splited = line.split()

                # We keep the name number in the node a id.
                # The reason we keep this and not an iter of how many nodes
                # we saw with something like enumerate() is because we need
                # to seperate the terminal nodes with the cell ones.
                # With this we can do really fast searches as such
                # e.g: node_list[a2_node_id] ---> Node("a2")
                node_name = line_splited[0]
                nodes_list.append(
                    Node(int(node_name[1:]) - 1, node_name, int(line_splited[1]), int(line_splited[2]))
                )
        return nodes_list

    def parse_nets(self) -> List[Net]:
        net_list: list[Net] = []

        with open(self.path_to_nets, "r") as net_file:
            pos_lines = net_file.readlines()[8:]

            net_id = 0
            nodes_names: List[str] = []
            for line in pos_lines:
                if line.startswith("NetDegree"):
                    net_list.append(Net(net_id, nodes_names))
                    net_id += 1
                    nodes_names: List[str] = []
                else:
                    line_splited = line.split()
                    nodes_names.append(line_splited[0])

            net_list.append(Net(net_id, nodes_names))
        return net_list

    def parse_rows(self) -> List[Row]:
        row_list: list[Row] = []
        with open(self.path_to_scl, "r") as rows_file:
            pos_lines = rows_file.readlines()[9:]
            y = x = height = x_end = -1

            for line in pos_lines:
                if line.startswith("CoreRow"):
                    row_list.append(Row(y, x, x_end, height))
                else:
                    line_splited = line.split()
                    if line_splited[0] == "Coordinate":
                        y = int(line_splited[-1])
                    elif line_splited[0] == "Height":
                        height = int(line_splited[-1])
                    elif line_splited[0] == "SubrowOrigin":
                        x = int(line_splited[2])
                        x_end = int(line_splited[-1])

        return row_list

    def parse_nodes_position(self) -> List[List[str]]:
        pos_list: list[list[str]] = []
        with open(self.path_to_pl, "r") as pos_file:
            pos_lines = pos_file.readlines()[2:]

            for line in pos_lines:
                line_splited = line.split()
                pos_list.append(line_splited[0:3])
        return pos_list
