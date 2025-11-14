import pygame as pg

TEXTURE_SCALE = (50, 50)

class Usable:
    COST = 0
    DELAY = 0
    def __init__(self) -> None:
        self.burn_limiter = 0
        self.spread_limiter = 0
        self.texture = None

    def update(self, cell):
        ...
    
    def render(self, surface, coords):
        surface.blit(self.texture, coords)

class Backburn(Usable):
    COST = 30
    DELAY = 10
    def __init__(self) -> None:
        super().__init__()
        self.burn_limiter = 0.3
        self.spread_limiter = 0.9

        self.texture = pg.transform.scale(pg.image.load("assets/images/usables/backburn.png"), TEXTURE_SCALE)

    def render(self, surface, coords):
        surface.blit(self.texture, coords)

class Wildcard(Usable):
    COST = 100
    DELAY = 10
    def __init__(self) -> None:
        super().__init__()
        self.burn_limiter = 1
        self.spread_limiter = 1
        self.texture = pg.transform.scale(pg.image.load("assets/images/usables/wildcard.png"), TEXTURE_SCALE)

class Fireman(Usable):
    COST = 15
    DELAY = 20
    def __init__(self) -> None:
        super().__init__()
        self.burn_limiter = 0.4
        self.spread_limiter = 0
        self.texture = pg.transform.scale(pg.image.load("assets/images/usables/fireman.png"), TEXTURE_SCALE)

    def update(self, cell):
        super().update(cell)
        if cell.fire > 0.3:
            cell.slot = Usable()

    
