HEAD_SW = 0
HEAD_W = 1
HEAD_NW = 2

HEAD_SE = 3
HEAD_E = 4
HEAD_NE = 5

HEAD_ALL = object()


class Action(object):
    def __init__(self, target):
        self.target = target

    def execute(self, head, state, time_now):
        raise NotImplemented()


class SetMotionMode(object):
    TRACKED = 'tracked'
    CONTROLLED = 'controlled'

    def __init__(self, target, mode):
        self.target = target
        self.mode = mode

    def execute(self, head, state, time_now):
        head.set_motion_mode(self.mode)


class PlayAudio(object):
    def __init__(self, target, file):
        self.target = target
        self.file = file

    def execute(self, head, state, time_now):
        head.play_audio(self.file)


class TurnToAngle(object):
    def __init__(self, target, angle, duration):
        self.target = target
        self.angle = angle
        self.duration = duration

    def execute(self, head, state, time_now):
        head.turn_to(self.angle, time_now + self.duration)


class TurnToPoint(object):
    def __init__(self, target, x, y, duration):
        self.target = target
        self.x = x
        self.y = y
        self.duration = duration

    def execute(self, head, state, time_now):
        head.turn_toward(self.x, self.y, time_now + self.duration)


class TurnToHead(object):
    def __init__(self, target, other_head, duration):
        self.target = target
        self.other_head = other_head
        self.duration = duration

    def execute(self, head, state, time_now):
        other_head = state.heads[self.other_head]
        # Avoid trying to turn to itself
        if other_head.x == head.x and other_head.y == head.y:
            return

        head.turn_toward(other_head.x, other_head.y, time_now + self.duration)
