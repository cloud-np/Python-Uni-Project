from classes.design import Design
from helpers.project_parser import Parser
import numpy as np
import matplotlib.pyplot as plt
from algos.legalizer import Legalizer
from algos.tetris import Tetris
from algos.swapper import Swapper
from classes.node import Node
from typing import List, Tuple
import pygame as pg


class EventType:
    """Enum that holds the types of events."""

    QUIT = -1
    NO_EVENT = 0
    RUN_TETRIS = 1
    RE_DRAW = 2
    MOUSE_BUTTONDOWN = 3
    MOUSE_BUTTONUP = 4
    RESET = 5
    RUN_EVERY_ALGO = 6
    SHOW_COLLISIONS_AND_CABLE = 7
    VANILLA_TETRIS = 8
    LR_TETRIS = 9
    LCU_TETRIS = 10
    RUN_SWAPPER = 11


class Visualizer:
    def __init__(self, design: Design, tetris: Tetris, legalizer: Legalizer, swapper: Swapper):
        self.design: Design = design
        self.clock = pg.time.Clock()
        self.is_running: bool = False
        self.tetris: Tetris = tetris
        self.run_swapper: bool = False
        self.run_tetris: bool = False
        self.legalizer = legalizer
        self.swapper = swapper
        self.nodes_info: List[str] = []
        self.delay: int = 50
        self.x_offset: int = 100
        self.y_offset: int = 20
        self.mltpl: int = 4  # multiplier to zoom-in or out
        self.canvas_width: int = 800
        self.canvas_height: int = 800
        pg.init()
        pg.display.set_caption('Chip Area')
        self.screen: pg.Surface = pg.display.set_mode((1200, 900))
        # In case of missing fonts.
        try:
            self.font = pg.font.Font('frontend/fonts/Roboto-Medium.ttf', 25)
        except(Exception):
            print("You are missing the font: 'Roboto-Medium.ttf'.\nA valid one from the system will be picked.")
            self.font = pg.font.Font(None, 15)
        self.bg_color: Tuple[int] = (17, 17, 17)
        self.no_info = self.font.render('', True, (255, 255, 255))

        self.screen.fill(self.bg_color)
        self.nodes_rect: List[pg.Rect] = []

        self.make_nodes_rect()

    def make_nodes_rect(self) -> None:
        """Creates the rectangulars for all the nodes to display on the screen."""
        # Reset the list
        self.nodes_rect: List[pg.Rect] = []
        for n in self.design.nodes:
            if not n.is_terminal:
                self.nodes_rect.append(pg.Rect(
                    (self.nrml_x(n.x), self.nrml_y(n.y), n.width * 4, n.height * 4)
                ))
            else:
                # y_adder: int = 10 if n.gid != 0 and n.gid != 1 else 0
                y_adder = 20
                self.nodes_rect.append(pg.Rect(
                    (self.nrml_x(n.x), self.nrml_y(n.y) + y_adder, (n.width * 4) + 5, (n.height * 4) + 5)
                ))

    def draw_rows(self) -> None:
        #         x      y    width   height
        # rect = (100,  200,   110,    200)
        color: Tuple[int] = (255, 255, 255)
        for row in self.design.rows:
            # nrml_x: int = self.canvas_height - self.x_offset
            nrml_y: int = self.nrml_y(row.y)
            pg.draw.line(
                self.screen, color, (self.nrml_x(row.x), nrml_y), (self.nrml_x(row.x_end), nrml_y)
            )

    def nrml_x(self, x):
        return ((x * self.mltpl) + self.x_offset)

    def nrml_y(self, y):
        return self.canvas_height - ((y * self.mltpl) + self.y_offset)

    def draw_nodes(self):
        for rect, n in zip(self.nodes_rect, self.design.nodes):
            pg.draw.rect(self.screen, n.color, rect)

    def reset(self, collisions, tetris_variant: Tuple[bool] = (False, False)):
        parser = Parser(design_path='./data/')
        design: Design = parser.parse_design()
        self.design = design
        self.tetris = Tetris(design, *tetris_variant)
        self.swapper = Swapper(design, 0, True)
        self.delay = 50
        self.run_tetris = False
        self.run_swapper = False
        self.legalizer = Legalizer(design)
        self.dehighlight_collisions(collisions)
        self.redraw_screen()

    def run_every_algo(self):
        return Tetris.run_every_tetris_variant()

    def run(self):
        self.is_running = True

        self.setup_screen()
        collisions = []
        while self.is_running:
            m_pos = pg.mouse.get_pos()

            event_code = Visualizer.check_for_events()
            if event_code == EventType.QUIT:
                self.is_running = False
            elif event_code == EventType.RUN_TETRIS:
                self.run_tetris = not self.run_tetris
            elif event_code == EventType.MOUSE_BUTTONUP:
                self.get_clicked_nodes(m_pos)
                # print(m_pos)
                self.setup_screen()
            elif event_code == EventType.RESET:
                self.reset(collisions)
            elif event_code == EventType.VANILLA_TETRIS:
                self.reset(collisions, tetris_variant=(False, False))
            elif event_code == EventType.LR_TETRIS:
                self.reset(collisions, tetris_variant=(False, True))
            elif event_code == EventType.LCU_TETRIS:
                self.reset(collisions, tetris_variant=(True, False))
            elif event_code == EventType.RUN_SWAPPER:
                self.run_swapper = True
            elif event_code == EventType.RUN_EVERY_ALGO:
                algos_info = self.run_every_algo()
                Visualizer.compare_tetrises(algos_info)
            elif event_code == EventType.RE_DRAW:
                self.dehighlight_collisions(collisions)
                self.redraw_screen()
            elif event_code == EventType.SHOW_COLLISIONS_AND_CABLE:
                self.show_collisions_and_cable_len()
            elif self.run_tetris:
                self.check_if_algo_ended(self.tetris.has_ended(), self.next_tetris_algo_step)
            elif self.tetris.has_ended() and self.run_swapper:
                self.check_if_algo_ended(self.swapper.has_ended(), self.next_swapper_algo_step)

            self.show_nodes_info()
            pg.display.update()

    def check_if_algo_ended(self, has_ended: bool, next_step_fnc):
        if not has_ended:
            next_step_fnc()
        else:
            if self.swapper.has_ended():
                self.delay = 0
                self.run_swapper = False
            self.run_tetris = False

    def next_swapper_algo_step(self):
        pg.time.wait(self.delay)
        self.redraw_screen()
        self.highlight_next_cell(self.swapper.get_curr_cell(), self.swapper.get_last_cell())
        self.swapper.next()

    def next_tetris_algo_step(self):
        # if self.tetris.has_ended():
        #     self.delay = 0
        pg.time.wait(self.delay)
        self.redraw_screen()
        self.highlight_next_cell(self.tetris.get_curr_cell(), self.tetris.get_last_cell())
        self.tetris.next()

    def show_collisions_and_cable_len(self):
        self.pause = True
        collisions = self.legalizer.find_collisions()
        txt = ''
        if len(collisions) == 0:
            txt += 'No collisions found! '
        else:
            self.highlight_collisions(collisions)
            self.redraw_screen()
        txt += f'Cable needed: {self.design.find_cable_needed()}'
        text = self.font.render(txt, True, (255, 255, 255))
        self.screen.blit(text, (580, 680))

    def dehighlight_cell(self, cell):
        cell.color = cell.og_color

    def dehighlight_collisions(self, collisions):
        for col in collisions:
            for c in col:
                c.color = c.og_color

    def highlight_collisions(self, collisions):
        nodes_col = []
        for col in collisions:
            for c in col:
                c.color = (255, 255, 255)
                if c not in nodes_col:
                    nodes_col.append(c)
        self.nodes_info = Visualizer.__nodes_to_str(nodes_col)

    def highlight_next_cell(self, cell, last_cell):
        if cell is not None:
            cell.color = (255, 255, 255)
            self.nodes_info = Visualizer.__nodes_to_str([cell])
        if last_cell is not None:
            self.dehighlight_cell(last_cell)
        self.redraw_screen()

    def redraw_screen(self) -> None:
        self.screen.fill(self.bg_color)
        self.make_nodes_rect()
        self.draw_nodes()
        self.draw_rows()

    def show_nodes_info(self):
        if len(self.nodes_info) == 0:
            return

        for i, info_arr in enumerate(self.nodes_info):
            txt = "".join(info_arr)

            # for txt in info_arr:
            text = self.font.render(txt, True, (255, 255, 255))
            self.screen.blit(text, (780, (80 + i * 50)))

    def get_clicked_nodes(self, m_pos):
        nodes_clicked: List[Node] = [node for rect, node in zip(self.nodes_rect, self.design.nodes) if rect.collidepoint(m_pos)]
        self.nodes_info = Visualizer.__nodes_to_str(nodes_clicked)

    @staticmethod
    def __nodes_to_str(nodes: List[Node]) -> List[str]:
        return [f"{n.name} w/h: ({n.width},{n.height}) pos: ({round(n.x, 2)},{round(n.y, 2)})" for n in nodes]

    def setup_screen(self):
        # Clear screen
        self.screen.fill(self.bg_color)
        # Draw the bare minimum.
        self.draw_rows()
        self.draw_nodes()

    @staticmethod
    def check_for_events():
        """Check for events that may occur during the game.

        Returns
        -------
        int
            An Event enum that shows which event occured if any.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return EventType.QUIT
            elif event.type == pg.MOUSEBUTTONDOWN:
                return EventType.MOUSE_BUTTONDOWN
            elif event.type == pg.MOUSEBUTTONUP:
                return EventType.MOUSE_BUTTONUP
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_9:
                    return EventType.RUN_EVERY_ALGO
                if event.key == pg.K_q:
                    return EventType.QUIT
                if event.key == pg.K_0:
                    return EventType.RESET
                if event.key == pg.K_1:
                    return EventType.VANILLA_TETRIS
                if event.key == pg.K_2:
                    return EventType.LR_TETRIS
                if event.key == pg.K_3:
                    return EventType.LCU_TETRIS
                if event.key == pg.K_z:
                    return EventType.RUN_SWAPPER
                if event.key == pg.K_c:
                    return EventType.SHOW_COLLISIONS_AND_CABLE
                if event.key == pg.K_t:
                    return EventType.RUN_TETRIS
                if event.key == pg.K_r:
                    return EventType.RE_DRAW

        return EventType.NO_EVENT

    @staticmethod
    def compare_tetrises(tetrises_info: dict, save_fig=False, show_fig=True):
        schedule_lens_x: List[int] = [round(t['cable_len']) for t in tetrises_info]

        # Change the color of the smallest schedule_len
        bar_colors = ['b' for _ in schedule_lens_x]
        min_len_index = schedule_lens_x.index(min(schedule_lens_x))
        bar_colors[min_len_index] = 'r'

        labels = [t['name'] for t in tetrises_info]

        plt.style.use("seaborn-dark")
        x = np.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots()

        rects = ax.bar(x - width / 2, schedule_lens_x, width, color=bar_colors)

        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        autolabel(rects, ax)
        ax.legend()
        ax.set_ylabel("Algo Used")
        # plt.grid(True)
        plt.title("Algorithms comparison for cable len")
        plt.grid(True)
        fig.set_size_inches(12, 4)
        fig.tight_layout()

        if show_fig:
            plt.show()
        if save_fig:
            plt.savefig("fig")
        return fig


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
