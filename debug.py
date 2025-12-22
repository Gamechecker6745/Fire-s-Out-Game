import pygame as pg


class Debug:
    def __init__(self, app) -> None:
        self.app = app
        self.fps = self.app.clock.get_fps()
        self.font = pg.font.SysFont("Arial", 20)
    
    def update(self):
        self.fps = self.app.clock.get_fps()
        self.app.display.surface.blit(self.font.render(str(self.fps), True, (255, 255, 255)), (10, 400))
        self.app.display.surface.blit(self.font.render(str(self.app.current_level.performance), True, (255, 255, 255)), (10, 450))
