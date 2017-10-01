from control.actions import HEAD_ALL
from control.scripts import AudioTest, AudioXTest, AudioYTest, HardwareTest, Track

class State:
    Rest = 'rest'
    Script = 'script'


class Director(object):
    start_time = 0.0

    script = None
    script_start_time = 0.0

    def __init__(self, now):
        self.start_time = now
        # self.start_script(AudioTest(), now)
        self.start_script(Track(), now)

    def direct(self, time_now, scene_state, input_state):
        # if input_state.present and self.script is None:
        #     self.start_script(AudioTest(), time_now)

        if self.script:
            self.advance_script(time_now, scene_state)

        self.update_tracking_heads(time_now, scene_state, input_state)

    def start_script(self, script, time_now):
        print("Starting script", script)
        self.script = script
        self.script_start_time = time_now

    def advance_script(self, time_now, scene_state):
        due_actions = self.script.get_due_actions(time_now - self.script_start_time)
        for action in due_actions:
            if action.target == HEAD_ALL:
                heads = scene_state.heads
            else:
                try:
                    heads = [scene_state.heads[action.target]]
                except IndexError:
                    continue

            for head in heads:
                action.execute(head, scene_state, time_now)

        if self.script.finished():
            print("Script ended", self.script)
            self.script = None

    def update_tracking_heads(self, time_now, scene_state, input_state):
        for head in scene_state.heads:
            if head.motion_mode == 'tracked':
                head.turn_toward(input_state.x, input_state.y, time_now + 0.5)
