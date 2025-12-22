import pygame as pg
import numpy as np


def align_position(surface, pos, align):
    match align:
        case 0:
            pass
        case 1:
            pos = pos - np.array(surface.get_size()) / 2
        case 2:
            pos = pos - np.array(surface.get_size())
        case _:
            raise TypeError('Invalid align value')
    return pos

class Default:
    def __init__(self, app, position, dimensions=None, surface=pg.Surface((0, 0)), action=None, args=tuple(), align=0, show_hover=False, hover_colour=(255, 255, 255), text=None) -> None:
        self.app = app

        self.action = action if action is not None else lambda:None
        self.args = args 

        self.hover_colour = hover_colour
        
        if dimensions is not None:
            self.dimensions = dimensions
            self.surface = pg.transform.scale(surface, dimensions)
        else:
            self.surface = surface
            self.dimensions = self.surface.get_size()

        self.align = align
        self.position = align_position(self.surface, position, align)
        self.rect = pg.Rect(self.position[0], self.position[1], self.dimensions[0], self.dimensions[1])
        self.show_hover = show_hover

    def update(self):
        self.render()

        # hover condition
        if self.rect.collidepoint(self.app.event.mouse_position):
            self.on_hover()

    def on_hover(self):
        # hover outline
        if self.show_hover:
            pg.draw.rect(self.app.display.surface, self.hover_colour, self.rect, 5)

        # hover function
        if self.app.event.left_click:
            self.on_click()

    def on_click(self):
        self.action(*self.args)

    def render(self):
        self.app.display.surface.blit(self.surface, self.position)

    # enables a surface to be reassigned for an object
    def update_surface(self, new_surface, update_dimensions=False):
        if update_dimensions:
            self.surface = new_surface
            self.dimensions = self.surface.get_size()
        else:
            self.surface = pg.transform.scale(new_surface, self.dimensions)