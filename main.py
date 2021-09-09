from helpers.project_parser import Parser
from algos.gordian import Gordian
from classes.design import Design
from frontend.visualizer import Visualizer
from algos.legalizer import Legalizer


if __name__ == "__main__":

    # parser = Parser(design_path='./data/test/')
    parser = Parser(design_path='./data/')
    design: Design = parser.parse_design()
    # Gordian(design=design, load_example=False).run()
    # Gordian(design=design, load_example=True).run()
    # # Visualizer(design=design)
    print(design.find_cable_needed())
    Visualizer(design=design).show_design()
    legalizer = Legalizer(design)
    print(design.find_cable_needed())
    # overlapping_pairs = Legalizer.check_for_overlaps(design.c_nodes)
    # legalizer.run_tetris()

    # Visualizer(design=design).test()
    # for node in nodes_list:
    #     print(node)
    # pos_list = parser.parse_nodes_position()

    # design.assign_pos_to_nodes(pos_list)
    # nodes = parser.parse_nodes()

    # nodes = [Node(i, f"a{i}", randint(2, 20), randint(2, 20)) for i in range(10)]
    # net = Net(0, set(nodes))
    # print(net)
