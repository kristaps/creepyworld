from boltons.mathutils import clamp

NUM_HEADS = 9


class HeadState(object):
    angle_start = 0.0
    angle_current = 0.0
    angle_end = 0.0

    time_start = 0.0
    time_current = 0.0
    time_end = 0.0

    def reset(self, duration=0.0):
        self.angle_start = self.angle_current = self.angle_end = 0.0
        self.time_start = self.time_current = self.time_end = 0.0

    def turn_to(self, angle, time_):
        self.angle_start = self.angle_current
        self.angle_end = angle

        self.time_start = self.time_current
        self.time_end = time_

    def update(self, time_now):
        self.time_current = time_now
        progress = clamp(
            (self.time_current -  self.time_start) / (self.time_end - self.time_start),
            0.0,
            1.0
        )
        self.angle_current = self.angle_start + progress * (self.angle_end - self.angle_start)


class SceneState(object):
    heads = [HeadState() for _ in range(NUM_HEADS)]

    def reset(self, duration=0.0):
        for head in self.heads:
            head.reset(duration)

    def update(self, time_now):
        for head in self.heads:
            head.update(time_now)


class InputState(object):
    x = 0.0
    y = 0.0
    present = False

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_presence(self, present):
        self.present = present
