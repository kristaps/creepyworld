

class State:
    Rest = 'rest'
    Script = 'script'


class Director(object):
    start_time = 0.0

    def __init__(self, now):
        self.start_time = now
        self.triggered = False
        self.triggered2 = False

    def direct(self, time_now, scene_state, input_state):
        for head in scene_state.heads:
            head.turn_toward(input_state.x, input_state.y)

        # if time_now - self.start_time > 3.0 and not self.triggered:
        #     print("TRIGGUURRRD!!")
        #     scene_state.heads[0].play_audio('test.ogg')
        #     self.triggered = True
        #
        # if time_now - self.start_time > 6.0 and not self.triggered2:
        #     print("TRIGGUURRRD2!!")
        #     scene_state.heads[5].play_audio('test2.ogg')
        #     self.triggered2 = True
