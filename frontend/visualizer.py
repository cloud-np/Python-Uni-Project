from classes.design import Design
from random import randint
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
        self.x_offset: int = 100
        self.y_offset: int = 12
        self.mltpl: int = 8  # multiplier to zoom-in or out
        self.screen = pg.display.set_mode((800, 800))
        color = (255, 255, 255)

        self.screen.fill(color)

    def draw_rows(self):
        #         x      y    width   height
        # rect = (100,  200,   110,    200)
        color = (0, 0, 0)
        for row in self.design.rows:
            # color = (randint(0, 255), randint(0, 255), randint(0, 255))
            pg.draw.line(
                self.screen, color, (self.x_offset, ((row.y - 100) + self.y_offset) * self.mltpl), (800 - self.x_offset, ((row.y - 100) + self.y_offset) * self.mltpl)
            )
            # rect = (row.x, row.y * i, row.width * 3, row.height * 3)
            # py_g.draw.rect(self.screen, color, rect)

        for c in self.design.c_nodes:
            pg.draw.rect(
                self.screen, c.color, ((c.x + self.x_offset), ((c.y - 100) + self.y_offset) * self.mltpl, c.width, c.height * 8)  # Maybe height * 8 is not right here but works for now.
            )

    def show_design(self):
        self.is_running = True

        self.draw_rows()
        while self.is_running:
            m_pos = pg.mouse.get_pos()

            event_code = Visualizer.check_for_events()
            if event_code == EventType.QUIT:
                self.is_running = False
            elif event_code == EventType.MOUSE_BUTTONUP:
                self.reveal_node_info(m_pos)
            pg.display.update()

    def reveal_node_info(self, m_pos):
        node = self.find_clicked_node(m_pos)

        ...

    def find_clicked_node(self, m_pos):

        ...

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
