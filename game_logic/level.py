import numpy as np


class Level:
    def __init__(self, map=((3,),), wind=(0, 0), budget=0, initial=((0,0),)) -> None:
        self.map = map
        self.wind = np.array(wind)
        self.budget = budget
        self.initial = initial
