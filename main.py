from helpers.project_parser import Parser
from algos.gordian import Gordian
from classes.design import Design
from algos.swapper import Swapper, SwapType
from frontend.visualizer import Visualizer
from helpers.dataframes import DataFrameMaker
from algos.legalizer import Legalizer
from algos.tetris import Tetris


if __name__ == "__main__":

    # parser = Parser(design_path='./data/test/')
    parser = Parser(design_path='./data/')
    design: Design = parser.parse_design()
    print(design.dfm)
    # Gordian(design=design, load_example=False).run()
    Gordian(design=design, load_example=True).run()

    # Auto run
    # tetris = Tetris(design, left_right=False, lower_cable_usage=False).run()
    # swapper = Swapper(design, SwapType.FIRST_FIT, is_checking=True).run()

    tetris = Tetris(design, left_right=False, lower_cable_usage=False)
    swapper = Swapper(design, SwapType.FIRST_FIT, is_checking=True)
    legalizer = Legalizer(design)

    Visualizer(design=design, tetris=tetris, legalizer=legalizer, swapper=swapper).run()

    # for df in design.get_dfs():
    #     print(df, end="\n\n")
    # overlapping_pairs = Legalizer.check_for_overlaps(design.c_nodes)
