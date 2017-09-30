class Action(object):
    def update(self, state):
        raise NotImplemented


class Track(object):
    pass


class PlayAudio(object):
    pass


class TurnToPoint(object):
    pass


class TurnToHead(TurnToPoint):
    pass
