from classes.design import Design
from classes.node import Node
from typing import List
import pygame as pg


class EventType:
    """Enum that holds the types of events."""

    QUIT = -1
    NO_EVENT = 0
    STOP = 1
    START = 2
    SHOW_INDEX = 3
    SHOW_NORMALIZED_INDEX = 4
    SHOW_IMGS = 5
    MOUSE_BUTTONDOWN = 6
    MOUSE_BUTTONUP = 7


class Visualizer:
    def __init__(self, design: Design):
        self.design = design
        self.clock = pg.time.Clock()
        self.is_running: bool = False
        self.nodes_info: List[str] = []
        self.x_offset: int = 100
        self.y_offset: int = 20
        self.mltpl: int = 8  # multiplier to zoom-in or out
        self.canvas_width = 800
        self.canvas_height = 800
        pg.init()
        pg.display.set_caption('Chip Area')
        self.screen = pg.display.set_mode((1200, 900))
        # In case of missing fonts.
        try:
            self.font = pg.font.Font('frontend/fonts/Roboto-Medium.ttf', 25)
        except(Exception):
            print("You are missing the font: 'Roboto-Medium.ttf'.\nA valid one from the system will be picked.")
            self.font = pg.font.Font(None, 15)
        self.bg_color = (17, 17, 17)
        self.no_info = self.font.render('', True, (255, 255, 255))

        self.screen.fill(self.bg_color)
        self.nodes_rect: List[pg.Rect] = list()

        # Make rectangles for all cell nodes in the screen
        for c in self.design.c_nodes:
            nrml_x = c.x + self.x_offset
            nrml_y = self.normalize_y(c.y)
            self.nodes_rect.append(pg.Rect(
                (nrml_x, nrml_y, c.width, c.height * 8)  # Maybe height * 8 is not right here but works for now.
            ))

    def draw_rows(self):
        #         x      y    width   height
        # rect = (100,  200,   110,    200)
        color = (255, 255, 255)
        for row in self.design.rows:
            nrml_x = self.canvas_height - self.x_offset
            nrml_y = self.normalize_y(row.y)
            pg.draw.line(
                self.screen, color, (self.x_offset, nrml_y), (nrml_x, nrml_y)
            )
            # rect = (row.x, row.y * i, row.width * 3, row.height * 3)
            # py_g.draw.rect(self.screen, color, rect)

    def normalize_y(self, y):
        return self.canvas_height - ((y - 100) + self.y_offset) * self.mltpl

    def draw_cells(self):
        for rect, n in zip(self.nodes_rect, self.design.c_nodes):
            pg.draw.rect(self.screen, n.color, rect)

        # for c in self.design.c_nodes:
        #     nrml_x = c.x + self.x_offset
        #     nrml_y = self.normalize_y(c.y)
        #     pg.draw.rect(
        #         self.screen, c.color, (nrml_x, nrml_y, c.width * 8, c.height * 8)  # Maybe height * 8 is not right here but works for now.
        #     )
        # Show terminal nodes.
        # for nt in self.design.t_nodes:
        #     pg.draw.circle(
        #         self.screen, nt.color, ((nt.x + self.x_offset), ((nt.y - 100) + self.y_offset)), radius=5
        #     )
        #     print(nt, f'--> ({(nt.x + self.x_offset)},{(nt.y - 100) + self.y_offset})')

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

    def show_clicked_node_info(self):

        if len(self.nodes_info) == 0:
            return

        for i, info_arr in enumerate(self.nodes_info):
            txt = "".join(info_arr)

            # for txt in info_arr:
            text = self.font.render(txt, True, (255, 255, 255))
            self.screen.blit(text, (780, (80 + i * 50)))

    def get_clicked_nodes(self, m_pos):
        nodes_clicked: List[Node] = [node for rect, node in zip(self.nodes_rect, self.design.c_nodes) if rect.collidepoint(m_pos)]
        self.nodes_info = [f"{n.name} w/h: ({n.width},{n.height}) pos: ({n.x},{n.y})" for n in nodes_clicked]

    def setup_screen(self):
        # Clear screen
        self.screen.fill(self.bg_color)
        # Draw the bare minimum.
        self.draw_rows()
        self.draw_cells()

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
                if event.key == pg.K_1:
                    return EventType.SHOW_INDEX
                if event.key == pg.K_2:
                    return EventType.SHOW_NORMALIZED_INDEX
                if event.key == pg.K_3:
                    return EventType.SHOW_IMGS

                #     pick_piece(mouse_x, mouse_y)
            # elif P2_COMPUTER and history['player'] % 2 != 0:
            #     self.pc_make_move(history, False)
            #     history['player'] += 1
        return EventType.NO_EVENT
