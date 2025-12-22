import pygame as pg
from time import perf_counter

from game_logic.tiles import *
from game_logic.usables import Backburn, Wildcard, Fireman, TEXTURE_SCALE

from display import render_text

TILE_SIZE = 40
INVENTORY_SPACING = (60, 60)
INVENTORY_POS = (300, 420)

class Level:
    def __init__(self, app, budget=100, template=None, starting_fires=None) -> None:
        self.app = app
        self.performance = None

        self.position = (300, 100)

        self.dragging = False
        self.dragged_object = None

        self.paused = True

        self.budget = budget

        self.delta_time = 0
        self.tick_speed = 20

        self.selected_tile = None
        self.selected_usable = None

        if template is None or len(template) == 0 or len(template[0]) == 0:
            self.template = [[3]]
        else:
            self.template = template

        self.map = []

        self.population = 0
        self.total_fire = 0
        self.has_started = False

        self.generate_map()
        if starting_fires is None:
            self.map[0][0].next_burn_state = 0.3
        else:
            for tile in starting_fires:
                self.map[tile[1]][tile[0]].next_burn_state = 0.3
        self.tick()

        

        self.inventory = [[Backburn(), Fireman()]]

    def generate_map(self):
        self.map = []

        for idy, y in enumerate(self.template):
            self.map.append([])
            for idx, x in enumerate(y):
                match x:
                    # arbituary tile type assignment
                    case 1:
                        new = Forest(self.app, self, (idx, idy))
                    case 2:
                        new = Plains(self.app, self, (idx, idy))
                    case 3:
                        new = Dwelling(self.app, self, (idx, idy))
                    case 4:
                        new = Road(self.app, self, (idx, idy))
                    case 0:
                        new = Tile(self.app, self, (idx, idy))
                self.map[idy].append(new)
    
    def update(self):
        self.performance = perf_counter()
        self.delta_time += self.app.delta_time
        if self.delta_time > 1 / self.tick_speed and not self.paused:
            self.tick()

        hovering_tile = False
        hovering_usable = False
        
        # tile loop
        for row in self.map:
               for tile in row:
                    tile.update(self.position, TILE_SIZE)
                    
                    # hovering
                    if tile.hovering:
                        hovering_tile = True
                        
                        # clicking
                        if self.app.event.left_click:
                            if self.selected_usable is not None and not isinstance(tile.slot, self.selected_usable.__class__) and not isinstance(tile.future_slot, self.selected_usable.__class__):
                                tile.set_slot(self.selected_usable)
                            else:
                                self.selected_tile = tile
                    tile.render(self.position, TILE_SIZE)

        # inventory loop
        y = INVENTORY_POS[1]
        x = INVENTORY_POS[0]
        for row in self.inventory:
            for item in row:
                item.render(self.app.display.surface, (x, y))
                if self.selected_usable is item:
                    pg.draw.rect(self.app.display.surface, (255, 255, 255), pg.Rect(x, y, TEXTURE_SCALE[0], TEXTURE_SCALE[1]), width=4)

                # hovering
                if pg.Rect(x,y, TEXTURE_SCALE[0], TEXTURE_SCALE[1]).collidepoint(self.app.event.mouse_position):
                    self.app.display.surface.blit(render_text(str(item.__class__.__name__), 15, (255, 255, 255)), (x, y - 30))
                    hovering_usable = True

                    # clicking
                    if self.app.event.left_click:
                        self.selected_usable = item
                x += INVENTORY_SPACING[0]
            y += INVENTORY_SPACING[1]
            x = INVENTORY_POS[0]

        # selecting conditions
        if not(hovering_usable or hovering_tile) and self.app.event.left_click:
            self.selected_usable = None
            self.selected_tile = None

        if self.population == 0:
            self.end_game()

        if round(self.total_fire, 2) == 0:
            if self.has_started:
                self.end_game()
            else:
                self.has_started = True

        # selected tile
        if self.selected_tile is not None:
            self.app.display.surface.blit(render_text(f"Fuel: {str(round(self.selected_tile.fuel, 1))}", 30, (255, 255, 0)), (20, 300))
            self.app.display.surface.blit(render_text(f"Fire: {str(round(self.selected_tile.fire, 1))}", 30, (255, 255, 0)), (20, 350))
            self.app.display.surface.blit(render_text(f"Slot: {str(self.selected_tile.slot.__class__.__name__)}", 30, (255, 255, 0)), (20, 400))
            if isinstance(self.selected_tile, Dwelling):
                self.app.display.surface.blit(render_text(f"Population: {str(self.selected_tile.population)}", 30, (255, 255, 0)), (20, 450))
        self.performance = perf_counter() - self.performance
                  
    def tick(self):
        for row in self.map:
                for tile in row:
                    tile.calculate()

        self.total_fire = 0
        for row in self.map:
            for tile in row:
                tile.tick()
                self.total_fire += tile.fire
            
        self.delta_time = 0

    def end_game(self):
        self.app.display.scene = "game_over"
