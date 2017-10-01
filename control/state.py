from boltons.mathutils import clamp
from math import atan2, pi

NUM_HEADS = 6

INITIAL_HEAD_POSITIONS = [
    (0.1, 0.6),
    (0.2, 0.8),
    (0.55, 0.85),
    (0.85, 0.85),

    # Initially planned setup, obviously didn't work out :)
    # (0.1, 0.1),  # SW
    # (0.1, 0.5),  # W
    # (0.1, 0.9),  # NW
    # (0.9, 0.1),  # SE
    # (0.9, 0.5),  # E
    # (0.9, 0.9),  # NE
    # (0.5, 0.1),  # S
    # (0.5, 0.5),  # Center
    # (0.5, 0.9),  # N
]


class HeadState(object):
    angle_start = 0.0
    angle_current = 0.0
    angle_end = 0.0

    time_start = 0.0
    time_current = 0.0
    time_end = 0.0

    x = 0.0
    y = 0.0

    audio_file = None
    volume = 0.5

    motion_mode = 'controlled'

    def reset(self, duration=0.0):
        self.angle_start = self.angle_current = self.angle_end = 0.0
        self.time_start = self.time_current = self.time_end = 0.0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def turn_to(self, angle, time_=None):
        self.angle_start = self.angle_current
        self.angle_end = angle

        self.time_start = self.time_current
        self.time_end = time_ or self.time_current

    def turn_toward(self, x, y, time_=None):
        angle = clamp((atan2(y - self.y, x - self.x) / pi * 180.0) + 180.0, 0.0, 360.0)
        self.turn_to(angle, time_)

    def set_motion_mode(self, mode):
        self.motion_mode = mode

    def play_audio(self, file):
        self.audio_file = file

    def update(self, time_now):
        self.time_current = time_now
        if self.time_end > self.time_start:
            progress = clamp(
                (self.time_current -  self.time_start) / (self.time_end - self.time_start),
                0.0,
                1.0
            )
        else:
            progress = 1.0

        self.angle_current = self.angle_start + progress * (self.angle_end - self.angle_start)


class SceneState(object):
    heads = [HeadState() for _ in range(NUM_HEADS)]

    def __init__(self):
        self.reset()
        for head, position in zip(self.heads, INITIAL_HEAD_POSITIONS):
            head.set_position(*position)

    def reset(self, duration=0.0):
        for head in self.heads:
            head.reset(duration)

    def update(self, time_now):
        for head in self.heads:
            head.update(time_now)


class InputState(object):
    x = 0.5
    y = 0.5
    present = False

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_presence(self, present):
        self.present = present
