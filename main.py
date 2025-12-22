import pygame as pg
pg.init()

from audio import Audio
from display import Display
from event import Event
from game_logic.level import Level
from debug import Debug

# level templates
LEVEL_1 = [[1,1,1,1,2],
           [1,1,1,2,2],
           [1,2,2,2,2],
           [2,2,1,2,2],
           [1,1,1,2,2],
           [1,3,3,1,2]]

LEVEL_2 = [[4,3,3,1,2,2,2],
           [4,4,4,1,1,1,2],
           [4,3,1,1,1,1,1],
           [4,3,1,1,1,1,1],
           [4,4,4,1,1,1,1],
           [4,3,3,1,1,1,1]]

class App:
    def __init__(self) -> None:
        self.running = False

        self.clock = pg.time.Clock()
        self.delta_time = 0

        self.reset_levels()

        # managers
        self.audio = Audio(self)
        self.display = Display(self)
        self.event = Event(self)
        self.debug = Debug(self)

    def reset_levels(self):
        self.levels = [Level(self, budget=180, template=LEVEL_1), 
                       Level(self, template=LEVEL_2, budget=200, starting_fires=((6,3),)), 
                       Level(self), Level(self, budget=300), 
                       Level(self, budget=600), 
                       Level(self, budget=500)]
        self.current_level = self.levels[0]

    def run(self):
        self.running = True
        self.audio.play_background()

        while self.running:
            self.update()

        self.on_exit()

    def update(self):
        self.delta_time = self.clock.tick() / 1000
        self.event.update()
        self.audio.update()
        self.display.update()

    def on_exit(self):
        ...

if __name__ == '__main__':
    app = App()
    app.run()