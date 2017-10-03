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



class Track(Script):
    ACTIONS = [
        (1.0, SetMotionMode(HEAD_ALL, SetMotionMode.TRACKED)),
    ]

# Setup motion mode before
# Use only head numbers [0,1,2,3]
class ProductionScript(Script):
    ACTIONS = [
        (10.0, SetMotionMode(HEAD_ALL, SetMotionMode.TRACKED)),
        (13.0, PlayAudio(0, 'ComeOn_01.wav')),  # 2 sec
        # +30 secs
        (35.0, PlayAudio(0, 'home_01.wav')),  # 2 sec (+3 sec)
        (38.0, PlayAudio(2, 'home_02.wav')),  # 7 sec (+8 sec)
        (46.0, PlayAudio(1, 'home_03.wav')),  # 9 sec (+10 sec)
        (56.0, PlayAudio(3, 'home_04.wav')),  # 3 sec
        # +18 secs
        # +18 secs
        (72.0, PlayAudio(0, 'ComeOn_03.wav')),  # 5 sec (+6 sec)
        (78.0, PlayAudio(2, 'ComeOn_04.wav')),  # 5 sec (+6 sec)
        (84.0, PlayAudio(1, 'ComeOn_05.wav')),  # 4 sec
        # + 20 secs
        (104.0, PlayAudio(0, 'garage48_part1.wav')),  # 4 sec (+5 sec)
        (109.0, PlayAudio(2, 'garage48-part2.wav')),  # 3 sec
    ]

class ProductionScriptBundled(Script):
    ACTIONS = [
        (10.0, SetMotionMode(HEAD_ALL, SetMotionMode.TRACKED)),
        (13.0, PlayAudio(0, 'ComeOn_01.wav')),  # 2 sec
        # +30 secs
        (35.0, PlayAudio(0, 'home_01.wav')),  # 2 sec (+3 sec)
        (38.0, PlayAudio(2, 'home_02.wav')),  # 7 sec (+8 sec)
        (46.0, PlayAudio(1, 'home_03.wav')),  # 9 sec (+10 sec)
        (56.0, PlayAudio(3, 'home_04.wav')),  # 3 sec
        # +18 secs
        # +18 secs
        (72.0, PlayAudio(0, 'ComeOn_03.wav')),  # 5 sec (+6 sec)
        (78.0, PlayAudio(2, 'ComeOn_04.wav')),  # 5 sec (+6 sec)
        (84.0, PlayAudio(1, 'ComeOn_05.wav')),  # 4 sec
        # + 20 secs
        (104.0, PlayAudio(0, 'garage48_part1.wav')),  # 4 sec (+5 sec)
        (109.0, PlayAudio(2, 'garage48-part2.wav')),  # 3 sec
    ]


class ProductionStep0(Script):
    ACTIONS = [
        (1.0, SetMotionMode(HEAD_ALL, SetMotionMode.TRACKED)),
        # (13.0, PlayAudio(0, 'ComeOn_01.wav')),  # 2 sec
    ]


class ProductionStep1(Script):
    ACTIONS = [
        (1.0, PlayAudio(0, 'home_01.wav')),  # 2 sec (+3 sec)
        (4.0, PlayAudio(2, 'home_02.wav')),  # 7 sec (+8 sec)
        (12.0, PlayAudio(1, 'home_03.wav')),  # 9 sec (+10 sec)
        (22.0, PlayAudio(3, 'home_04.wav')),  # 3 sec
    ]


class ProductionStep2(Script):
    ACTIONS = [
        (1.0, PlayAudio(0, 'ComeOn_03.wav')),  # 5 sec (+6 sec)
        (7.0, PlayAudio(2, 'ComeOn_04.wav')),  # 5 sec (+6 sec)
        (13.0, PlayAudio(1, 'ComeOn_05.wav')),  # 4 sec
    ]


class ProductionStep3(Script):
    ACTIONS = [
        (0.0, PlayAudio(0, 'garage48_part1.wav')),  # 4 sec (+5 sec)
        (5.0, PlayAudio(2, 'garage48-part2.wav')),  # 3 sec
    ]


# class Production2Script(Script):
#     ACTIONS = [
#         (10.0, SetMotionMode(HEAD_ALL, SetMotionMode.TRACKED)),
#
#         (13.0, PlayAudio(0, 'hello_01.wav')),  # 1 sec (+2 sec)
#         (14.5, PlayAudio(3, 'hello_02.wav')),  # 1 sec (+2 sec)
#         # +30 secs
#         (35.0, PlayAudio(0, 'home_01.wav')),  # 2 sec (+3 sec)
#         (38.0, PlayAudio(2, 'home_02.wav')),  # 7 sec (+8 sec)
#         (46.0, PlayAudio(1, 'home_03.wav')),  # 9 sec (+10 sec)
#         (56.0, PlayAudio(3, 'home_04.wav')),  # 3 sec
#         # +18 secs
#         (72.0, PlayAudio(0, 'ComeOn_03.wav')),  # 5 sec (+6 sec)
#         (78.0, PlayAudio(2, 'ComeOn_04.wav')),  # 5 sec (+6 sec)
#         (84.0, PlayAudio(1, 'ComeOn_05.wav')),  # 4 sec
#         # + 20 secs
#         (104.0, PlayAudio(0, 'garage48_part1.wav')),  # 4 sec (+5 sec)
#         (109.0, PlayAudio(2, 'garage48-part2.wav')),  # 3 sec
#
#         # (120.0, PlayAudio(3, 'laugh_04.wav')),  # 7 sec (+2 sec)
#         # (122.0, PlayAudio(1, 'laugh_03.wav')),  # 5 sec (+1 sec)
#         # (123.0, PlayAudio(0, 'laugh_01.wav')),  # 7 sec (+0 sec)
#     ]
