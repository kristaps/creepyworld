from .actions import *


class Script(object):
    ACTIONS = []

    def __init__(self):
        self.actions = self.ACTIONS[:]

    def get_due_actions(self, time_now):
        actions = []
        while self.actions and time_now >= self.actions[0][0]:
            actions.append(self.actions.pop(0)[1])

        return actions

    def finished(self):
        return not bool(self.actions)


class HardwareTest(Script):
    ACTIONS = [
        (1.0, TurnToAngle(HEAD_ALL, 0.0, 3.0)),
        (5.0, TurnToAngle(HEAD_ALL, 90.0, 3.0)),
        (9.0, TurnToAngle(HEAD_ALL, 180.0, 3.0)),
        (13.0, TurnToAngle(HEAD_ALL, 270.0, 3.0)),
        (17.0, TurnToAngle(HEAD_ALL, 0.0, 3.0)),
        (21.0, PlayAudio(0, 'id0.wav')),
        (24.0, PlayAudio(1, 'id1.wav')),
        (27.0, PlayAudio(2, 'id2.wav')),
        (30.0, PlayAudio(3, 'id3.wav')),
        (33.0, PlayAudio(4, 'id4.wav')),
        (36.0, PlayAudio(5, 'id5.wav')),
    ]


class AudioTest(Script):
    ACTIONS = [
        (1.0, PlayAudio(0, 'id0.wav')),
        (3.0, PlayAudio(1, 'id1.wav')),
        (5.0, PlayAudio(2, 'id2.wav')),
        (7.0, PlayAudio(3, 'id3.wav')),
        (9.0, PlayAudio(4, 'id4.wav')),
        (11.0, PlayAudio(5, 'id5.wav')),
    ]

class AudioXTest(Script):
    ACTIONS = [
        (1.0, PlayAudio(0, 'id1.wav')),
        (3.0, PlayAudio(3, 'id1.wav')),
    ]


class AudioYTest(Script):
    ACTIONS = [
        (1.0, PlayAudio(3, 'id1.wav')),
        (3.0, PlayAudio(5, 'id1.wav')),
    ]
