import pygame as pg
pg.init()

from audio import Audio
from display import Display
from event import Event
from game_logic.game import Game
from game_logic.level import Level
from debug import Debug

# level templates
LEVEL_1 = Level([[1,1,1,1,2],
                 [1,1,1,2,2],
                 [1,2,2,2,2],
                 [2,2,1,2,2],
                 [1,1,1,2,2],
                 [1,3,3,1,2]], budget=180)

LEVEL_2 = Level([[4,3,3,1,2,2,2],
                 [4,4,4,1,1,1,2],
                 [4,3,1,1,1,1,1],
                 [4,3,1,1,1,1,1],
                 [4,4,4,1,1,1,1],
                 [4,3,3,1,1,1,1]], budget=200, initial=((6,3),))

LEVEL_3 = Level([[4,3,3,1,2,2,2],
                 [4,4,4,1,1,1,2],
                 [4,3,1,1,1,1,1],
                 [4,3,1,1,1,1,1],
                 [4,4,4,1,1,1,1],
                 [4,3,3,1,1,1,1]], budget=200, initial=((6,3),), wind=(-1.5,0))

class App:
    def __init__(self) -> None:
        self.running = False

        self.clock = pg.time.Clock()
        self.delta_time = 0

        self.levels = LEVEL_1, LEVEL_2, LEVEL_3

        # managers
        self.game = Game(self)
        self.audio = Audio(self)
        self.display = Display(self)
        self.event = Event(self)
        self.debug = Debug(self)

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
    
    def exit_game(self):
        self.running = False

if __name__ == '__main__':
    app = App()
    app.run()