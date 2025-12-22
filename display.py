import pygame as pg
from time import perf_counter

from settings import *
from sprites.default import Default
from subscription import Subsciber

# button surface creation
levels_button = pg.Surface((200, 200))
pg.draw.circle(levels_button, (180, 250, 0), (100, 100), 100)
tutorial_button = pg.image.load("assets/images/buttons/tutorial.png")
settings_button = pg.image.load("assets/images/buttons/settings.png")
menu_button = pg.Surface((30, 30))
menu_button.fill((255, 255, 255))
menu_button.blit(pg.transform.scale(pg.image.load("assets/images/buttons/menu.png"), menu_button.get_size()), (0, 0))

exit_button = pg.image.load("assets/images/buttons/exit.png")

def switch_scene(app, scene):
    if scene == "menu":
        app.reset_levels()
        app.display.scenes['game'][0] = app.current_level
        app.display.scenes['levels'] = [Default(app, (50 + 400*(idx%2), 50 + 50 * (idx - idx%2)), surface=render_text(f"L{idx + 1}", 50, (255, 255, 255)), show_hover=True, action=select_level, args=(app,level)) for idx, level in enumerate(app.levels)] + \
                                       [Default(app, (WIDTH - 5, menu_button.get_height() + 5), surface=menu_button, align=2, action=switch_scene, args=(app, "menu"), show_hover=True, hover_colour=(255, 255, 0))]
        app.audio.play_background()
    elif scene != "settings":
        app.audio.stop_background()
    app.display.scene = scene

def render_text(text, size, colour):
    font = pg.font.SysFont('Arial', size)
    return font.render(text, True, colour)

def toggle_pause(app):
    app.current_level.paused = not app.current_level.paused

def speed_change(app, factor):
    app.current_level.tick_speed *= factor

def next_tick(app):
    app.current_level.tick()

def leave(app):
    app.running = False

def select_level(app, level):
    app.current_level = level
    app.display.scenes['game'][0] = app.current_level
    app.display.scenes['levels'] = [Default(app, (50 + 400*(idx%2), 50 + 50 * (idx - idx%2)), surface=render_text(f"L{idx + 1}", 50, (255, 255, 255)), show_hover=True, action=select_level, args=(app,level)) for idx, level in enumerate(app.levels)]
    switch_scene(app, "game")

class Display:
    def __init__(self, app) -> None:
        self.app = app

        self.scenes = {"menu": [Default(self.app, (400, 80), align=1, surface=render_text("Fire's Out", 80, (255, 255, 255))),
                                Default(self.app, (200, 300), align=1, surface=levels_button, show_hover=True, action=switch_scene, args=(self.app,"levels")),
                                Default(self.app, (200, 300), align=1, surface=render_text("Levels", 50, (0, 0, 0))),
                                Default(self.app, (600, 200), dimensions=(200, 75), align=1, surface=tutorial_button, action=switch_scene, args=(self.app, "tutorial"), show_hover=True),
                                Default(self.app, (600, 300), dimensions=(200, 75), surface=settings_button, align=1, action=switch_scene, args=(self.app, "settings"), show_hover=True),
                                Default(self.app, (600, 400), dimensions=(200, 75), surface=exit_button, align=1, action=leave, args=(self.app,), show_hover=True)],
                       "tutorial": [Default(self.app, (0, 0), DEFAULT_DIMENSIONS, pg.image.load("assets/images/tutorial.png")),
                                    Default(self.app, (WIDTH - 5, menu_button.get_height() + 5), surface=menu_button, align=2, action=switch_scene, args=(self.app, "menu"), show_hover=True, hover_colour=(255, 255, 0))],
                       "settings":[Default(self.app, (WIDTH - 5, menu_button.get_height() + 5), surface=menu_button, align=2, action=switch_scene, args=(self.app, "menu"), show_hover=True, hover_colour=(255, 255, 0)),],
                       "levels":[Default(self.app, (50 + 400*(idx%2), 50 + 50 * (idx - idx%2)), surface=render_text(f"L{idx + 1}", 50, (255, 255, 255)), show_hover=True, action=select_level, args=(self.app,level)) for idx, level in enumerate(self.app.levels)] + 
                                [Default(self.app, (WIDTH - 5, menu_button.get_height() + 5), surface=menu_button, align=2, action=switch_scene, args=(self.app, "menu"), show_hover=True, hover_colour=(255, 255, 0))],
                       "game": [self.app.current_level,
                                Default(self.app, (600, 50), dimensions=(50, 50), surface=render_text("||", 500, (255, 255, 255)), action=toggle_pause, args=(self.app,), show_hover=True, align=1),
                                Default(self.app, (650, 50), dimensions=(50, 50), surface=render_text(">>", 500, (255, 255, 255)), action=speed_change, args=(self.app,2), show_hover=True, align=1),
                                Default(self.app, (550, 50), dimensions=(50, 50), surface=render_text("<<", 500, (255, 255, 255)), action=speed_change, args=(self.app,1/2), show_hover=True, align=1),
                                Default(self.app, (600, 150), surface=render_text("next tick", 20, (255, 255, 255)), action=next_tick, args=(self.app,), show_hover=True, align=1),
                                Default(self.app, (20, 50), surface=render_text(f"Budget: {str(self.app.current_level.budget)}", 30, (255, 255, 255))),
                                Default(self.app, (20, 100), surface=render_text(f"Population: {str(self.app.current_level.population)}", 30, (255, 255, 255))),
                                Default(self.app, (20, 150), surface=render_text(f"Total fire: {str(round(self.app.current_level.total_fire, 2))}", 30, (255, 255, 255))),
                                Default(self.app, (WIDTH - 5, menu_button.get_height() + 5), surface=menu_button, align=2, action=switch_scene, args=(self.app, "menu"), show_hover=True, hover_colour=(255, 255, 0)),],
                        "game_over": [Default(self.app, (WIDTH - 5, menu_button.get_height() + 5), surface=menu_button, align=2, action=switch_scene, args=(self.app, "menu"), show_hover=True, hover_colour=(255, 255, 0)),
                                      Default(self.app, (20, 150), surface=render_text(f"Budget: {str(self.app.current_level.budget)}", 30, (255, 255, 255))),
                                      Default(self.app, (20, 200), surface=render_text(f"Population: {str(self.app.current_level.population)}", 30, (255, 255, 255))),
                                      Default(self.app, (20, 250), surface=render_text(f"Fire: {str(round(self.app.current_level.total_fire, 1))}", 30, (255, 255, 255)))]}
        self.scene = "menu"
        
        self.screen = pg.display.set_mode(DEFAULT_DIMENSIONS)
        pg.display.set_caption(CAPTION)
        self.surface = pg.Surface(DEFAULT_DIMENSIONS)

    def update(self):
        performance = perf_counter()
        self.surface.fill((0, 0, 0))

        match self.scene:
                case "game":
                    self.scenes[self.scene][5].update_surface(render_text(f"Budget: {str(self.app.current_level.budget)}", 30, (255, 255, 255)), update_dimensions=True)
                    self.scenes[self.scene][6].update_surface(render_text(f"Population: {str(self.app.current_level.population)}", 30, (255, 255, 255)), update_dimensions=True)
                    self.scenes[self.scene][7].update_surface(render_text(f"Total fire: {str(round(self.app.current_level.total_fire, 2))}", 30, (255, 255, 255)), update_dimensions=True)
                case "game_over":
                    self.scenes[self.scene][1].update_surface(render_text(f"Budget: {str(self.app.current_level.budget)}", 30, (255, 255, 255)))
                    self.scenes[self.scene][2].update_surface(render_text(f"Population: {str(self.app.current_level.population)}", 30, (255, 255, 255)))
                    self.scenes[self.scene][3].update_surface(render_text(f"Fire: {str(round(self.app.current_level.total_fire, 1))}", 30, (255, 255, 255)), update_dimensions=True)

        # scene loop
        for sprite in self.scenes[self.scene]:
            sprite.update()

        self.screen.blit(self.surface, (0, 0))
        pg.display.flip()
        print(perf_counter() - performance)

    