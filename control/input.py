from time import time
from math import sin, cos


class InputController(object):
    x = 0.0
    y = 0.0

    def __init__(self):
        self.init_time = time()

    def update_input(self, state):
        # TODO: replace with actual input
        now = time()
        state.x = round(sin(now - self.init_time) / 2.0, 4)
        state.y = round(cos(now - self.init_time) / 2.0, 4)
