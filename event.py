import pygame as pg


class Event:
    def __init__(self, app) -> None:
        self.app = app

        self.mouse_position = (0, 0)
        self.left_click = False

    def update(self):
        self.left_click = False
        self.mouse_position = pg.mouse.get_pos()
        self.mouse_buttons = pg.mouse.get_pressed()

        events = pg.event.get()

        for event in events:
            match event.type:
                case pg.QUIT:
                    self.app.running = False
                case pg.MOUSEBUTTONDOWN:
                    match event.button:
                        case 1:
                            self.left_click = True
