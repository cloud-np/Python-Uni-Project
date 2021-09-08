from classes.design import Design
from classes.node import Node
from typing import List, Tuple
import pygame as pg


class EventType:
    """Enum that holds the types of events."""

    QUIT = -1
    NO_EVENT = 0
    STOP = 1
    START = 2
    MOUSE_BUTTONDOWN = 3
    MOUSE_BUTTONUP = 4
    ZOOM_IN = 5
    ZOOM_OUT = 6


class Visualizer:
    def __init__(self, design: Design):
        self.design: Design = design
        self.clock = pg.time.Clock()
        self.is_running: bool = False
        self.nodes_info: List[str] = []
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
        self.nodes_rect: List[pg.Rect] = list()

        self.make_nodes_rect()

    def make_nodes_rect(self) -> None:
        """Creates the rectangulars for all the nodes to display on the screen."""
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

    # def draw_terminals(self) -> None:
    #     for t in self.design.t_nodes:
    #         pg.draw.circle(self.screen, t.color, (t.x, t.y), 10)

    def draw_rows(self) -> None:
        #         x      y    width   height
        # rect = (100,  200,   110,    200)
        color: Tuple[int] = (255, 255, 255)
        for row in self.design.rows:
            nrml_x: int = self.canvas_height - self.x_offset
            nrml_y: int = self.nrml_y(row.y)
            pg.draw.line(
                self.screen, color, (self.x_offset, nrml_y), (nrml_x, nrml_y)
            )

    def nrml_x(self, x):
        return ((x * self.mltpl) + self.x_offset)

    def nrml_y(self, y):
        return self.canvas_height - ((y * self.mltpl) + self.y_offset)

    def draw_nodes(self):
        for rect, n in zip(self.nodes_rect, self.design.nodes):
            pg.draw.rect(self.screen, n.color, rect)

    def show_design(self):
        self.is_running = True

        self.setup_screen()
        while self.is_running:
            m_pos = pg.mouse.get_pos()

            event_code = Visualizer.check_for_events()
            if event_code == EventType.QUIT:
                self.is_running = False
            elif event_code == EventType.MOUSE_BUTTONUP:
                self.get_clicked_nodes(m_pos)
                print(m_pos)
                self.setup_screen()
            self.show_clicked_node_info()

            # self.screen.blit(self.nodes_info, (780, 100))
            # text = self.font.render(msg, True, (255, 255, 255))
            pg.display.update()
            # elif event_code == EventType.ZOOM_IN:

    def draw_middle_point(self):
        ...

    def show_clicked_node_info(self):
        if len(self.nodes_info) == 0:
            return

        for i, info_arr in enumerate(self.nodes_info):
            txt = "".join(info_arr)

            # for txt in info_arr:
            text = self.font.render(txt, True, (255, 255, 255))
            self.screen.blit(text, (780, (80 + i * 50)))

    def get_clicked_nodes(self, m_pos):
        nodes_clicked: List[Node] = [node for rect, node in zip(self.nodes_rect, self.design.nodes) if rect.collidepoint(m_pos)]
        self.nodes_info = [f"{n.name} w/h: ({n.width},{n.height}) pos: ({n.x},{n.y})" for n in nodes_clicked]

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
                if event.key == pg.K_q:
                    return EventType.QUIT
                if event.key == pg.K_1:
                    return EventType.ZOOM_IN
                if event.key == pg.K_2:
                    return EventType.ZOOM_OUT

        return EventType.NO_EVENT
