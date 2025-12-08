import random as rn
import pygame as pg
from time import perf_counter

from game_logic.usables import *

SURVIVAL_FUEL = 0.5

FONT = pg.font.SysFont("Arial", 15, False, False)

def get_usable_border(usable):
    # border identification if usable present
    if isinstance(usable, Wildcard):
        border = (255, 0, 0)
    elif isinstance(usable, Backburn):
        border = (128, 128, 128)
    elif isinstance(usable, Fireman):
        border = (0, 10, 200)
    elif isinstance(usable, Usable):
        border = (0, 0, 0)
    else:
        border = (255, 0, 255)
    return border

class Tile:
    BURN_RATE = 0.1
    SPREAD_RATE = 0.1
    BURN_DURATION = 100
    TEXTURE = pg.image.load("assets/images/tiles/default.png")

    def __init__(self, app, game, position) -> None:
        self.app = app
        self.game = game

        self.hovering = False

        self.position = position
        self.next_position = position

        self.slot = Usable()
        self.slot_delay = 0
        self.future_slot = None

        self.burn_array = []

        self.burn_state = 0
        self.fire = 0
        self.fuel = 1
        self.next_burn_state = 0

        self.spreadability = 0.8
        self.consumption = 0

    def calculate(self):
        # fire spread within cell
        self.next_burn_state += self.fire * self.__class__.BURN_RATE * (1-self.slot.burn_limiter) * rn.random()

        # fire spread between cells
        if self.position[1] - 1 >= 0:
            self.next_burn_state += self.game.map[self.position[1] - 1][self.position[0]].fire * rn.random() * 0.05 * (1-self.slot.spread_limiter) * self.__class__.SPREAD_RATE
        if self.position[0] - 1 >= 0:
            self.next_burn_state += self.game.map[self.position[1]][self.position[0] - 1].fire * rn.random() * 0.05 * (1-self.slot.spread_limiter) * self.__class__.SPREAD_RATE
        if self.position[1] + 1 < len(self.game.map):
            self.next_burn_state += self.game.map[self.position[1] + 1][self.position[0]].fire * rn.random() * 0.05 * (1-self.slot.spread_limiter) * self.__class__.SPREAD_RATE
        if self.position[0] + 1 < len(self.game.map[self.position[1]]): 
            self.next_burn_state += self.game.map[self.position[1]][self.position[0] + 1].fire * rn.random() * 0.05 * (1-self.slot.spread_limiter) * self.__class__.SPREAD_RATE

        if self.next_burn_state > 1 or 1 - self.next_burn_state < 0.001:
            self.next_burn_state = 1
        elif self.next_burn_state < 0.001:
            self.next_burn_state = 0

        if (burnt_material := self.next_burn_state - self.burn_state) != 0:
            self.burn_array.append([burnt_material, self.__class__.BURN_DURATION])
    
    def tick(self):
        self.position = self.next_position
        self.burn_state = self.next_burn_state

        for idx, log in enumerate(self.burn_array):
            log[1] -= 1
            if log[1] == 0:
                self.fuel -= self.burn_array.pop(idx)[0]

        # slot mangement
        self.slot_delay -= 1
        if self.slot_delay <= 0 and self.future_slot is not None:
            self.slot_delay = 0
            self.slot = self.future_slot
            self.future_slot = None

        self.fire = self.burn_state + self.fuel - 1

    def set_slot(self, usable):
        if self.game.budget - usable.__class__.COST >= 0:
            self.slot_delay = usable.__class__.DELAY
            self.future_slot = usable
            self.game.budget -= usable.__class__.COST

    def update(self, map_position, side_length):
        if pg.Rect(map_position[0] + side_length*self.position[0], map_position[1] + side_length*self.position[1], side_length, side_length).collidepoint(self.app.event.mouse_position):
            self.hovering = True
        else:
            self.hovering = False

        self.slot.update(self)

    def render(self, map_position, side_length):
        if self.hovering or self.game.selected_tile is self:
            border  = (255, 255, 255)
        else:
            border = get_usable_border(self.slot)

        self.app.display.surface.blit(pg.transform.scale(self.__class__.TEXTURE, (side_length, side_length)), (map_position[0] + side_length*self.position[0], map_position[1] + side_length*self.position[1]))
        fire_filter = pg.Surface((side_length, side_length))
        fire_filter.fill((255, 0, 0))
        fire_filter.set_alpha(220 * self.fire)

        burn_fliter = pg.Surface((side_length, side_length))
        burn_fliter.fill((0, 0, 0))
        burn_fliter.set_alpha(220 * (1-self.fuel))

        self.app.display.surface.blit(fire_filter, (map_position[0] + side_length*self.position[0], map_position[1] + side_length*self.position[1]))
        self.app.display.surface.blit(burn_fliter, (map_position[0] + side_length*self.position[0], map_position[1] + side_length*self.position[1]))
        pg.draw.rect(self.app.display.surface, border, pg.Rect(map_position[0] + side_length*self.position[0], map_position[1] + side_length*self.position[1], side_length, side_length), width=4)

        if self.slot_delay > 0:
            text = FONT.render(str(self.slot_delay), True, (255, 255, 255), (0, 0, 0))
            self.app.display.surface.blit(text, (map_position[0] + side_length*self.position[0], map_position[1] + side_length*self.position[1]))

class Forest(Tile):
    BURN_RATE = 0.1
    SPREAD_RATE = 0.6
    BURN_DURATION = 20
    TEXTURE = pg.image.load("assets/images/tiles/forest.png")

class Plains(Tile):
    BURN_RATE = 0.9
    SPREAD_RATE = 1
    BURN_DURATION = 3
    TEXTURE = pg.image.load("assets/images/tiles/plains.png")

class Dwelling(Tile):
    BURN_RATE = 0.3
    SPREAD_RATE = 0.3
    BURN_DURATION = 35
    TEXTURE = pg.image.load("assets/images/tiles/dwelling.png")

    def __init__(self, app, game, position, population=1) -> None:
        super().__init__(app, game, position)
        self.capacity = population
        self.population = population
        self.game.population += population

    def tick(self):
        super().tick()
        if self.fuel < 0.3 and self.capacity == self.population:
            self.population = 0
            self.game.population -= self.capacity

    def set_slot(self, usable):
        if self.game.budget - usable.__class__.COST >= 0 and not isinstance(usable, Backburn):
            self.slot = usable
            self.game.budget -= usable.__class__.COST


class Road(Tile):
    BURN_DURATION = 1
    SPREAD_RATE = 0.1
    BURN_RATE = 0
    TEXTURE = pg.image.load("assets/images/tiles/road.png")

    
