from classes.node import Node
from classes.design import Design
from classes.net import Net
from classes.row import Row
from typing import List


class Parser:
    def __init__(
        self,
        design_path: str = "./data/",
        nets_fname: str = "design.nets",
        nodes_fname: str = "design.nodes",
        pl_fname: str = "design.pl",
        scl_fname: str = "design.scl",
    ):
        self.path_to_nets = design_path + nets_fname
        self.path_to_nodes = design_path + nodes_fname
        self.path_to_pl = design_path + pl_fname
        self.path_to_scl = design_path + scl_fname

    def parse_design(self):
        nodes_list = self.parse_nodes()
        nodes_pos = self.parse_nodes_position()
        net_list = self.parse_nets()
        row_list = self.parse_rows()
        return Design(0, set(net_list), nodes_list, nodes_pos, row_list)

    def parse_nodes(self):
        # Make list here with size of len(nodes)
        nodes_list: list[Node] = []
        with open(self.path_to_nodes, "r") as nodes_file:
            nodes_lines = nodes_file.readlines()[7:]

            for i, line in enumerate(nodes_lines):
                line_splited = line.split()

                # We keep the name number in the node a gid (group_id Look for more details in node.py).
                # The reason we keep this and not only an iter of how many nodes
                # is to seperate the terminal nodes with the cell ones.
                # With this we can do really fast searches as such
                # e.g: terminal_nodes_only[p2_node_gid] ---> Node("p2")
                node_name = line_splited[0]
                nodes_list.append(
                    Node(id_=i, gid=int(node_name[1:]) - 1, name=node_name, width=int(line_splited[1]), height=int(line_splited[2]))
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

            id_ = 0
            for line in pos_lines:
                if line.startswith("CoreRow"):
                    row_list.append(Row(id_, y, x, x_end, height))
                    id_ += 1
                else:
                    line_splited = line.split()
                    if line_splited[0] == "Coordinate":
                        y = int(line_splited[-1])
                    elif line_splited[0] == "Height":
                        height = int(line_splited[-1])
                    elif line_splited[0] == "SubrowOrigin":
                        x = int(line_splited[2])
                        x_end = int(line_splited[-1])

        row_list.append(Row(id_, y, x, x_end, height))
        return row_list

    def parse_nodes_position(self) -> List[List[str]]:
        pos_list: list[list[str]] = []
        with open(self.path_to_pl, "r") as pos_file:
            pos_lines = pos_file.readlines()[2:]

            for line in pos_lines:
                line_splited = line.split()
                pos_list.append(line_splited[0:3])
        return pos_list
