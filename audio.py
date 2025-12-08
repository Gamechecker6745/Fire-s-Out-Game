# Epic Cinematic Trailer | ELITE by Alex-Productions | https://onsound.eu/
# Music promoted by https://www.chosic.com/free-music/all/
# Creative Commons CC BY 3.0
# https://creativecommons.org/licenses/by/3.0/

import pygame as pg

class Audio:
    def __init__(self, app) -> None:
        self.app = app
        pg.mixer.music.load("assets/audio/background_menu.mp3")
        pg.mixer.music.set_volume(0.1)

        self.sound_effects: dict[pg.mixer.Sound] = {"backburn": pg.mixer.Sound("assets/audio/backburn.mp3")}
    
    def play_background(self):
        pg.mixer.music.play()

    def stop_background(self):
        pg.mixer.music.stop()

    def play_sound_effect(self, id):
        self.sound_effects[id].set_volume(0.1)
        self.sound_effects[id].play()

    def update(self):
        ...
