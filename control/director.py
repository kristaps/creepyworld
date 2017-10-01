from control.actions import HEAD_ALL
from control.scripts import AudioTest, AudioXTest, HardwareTest

class State:
    Rest = 'rest'
    Script = 'script'


class Director(object):
    start_time = 0.0

    script = None
    script_start_time = 0.0

    def __init__(self, now):
        self.start_time = now
        self.start_script(HardwareTest(), now)

    def direct(self, time_now, scene_state, input_state):
        if self.script:
            self.advance_script(time_now, scene_state)

        # TODO: turn heads that are tracking

    def start_script(self, script, time_now):
        print("Starting script", self.script)
        self.script = script
        self.script_start_time = time_now

    def advance_script(self, time_now, scene_state):
        due_actions = self.script.get_due_actions(time_now - self.script_start_time)
        for action in due_actions:
            if action.target == HEAD_ALL:
                heads = scene_state.heads
            else:
                heads = [scene_state.heads[action.target]]

            for head in heads:
                action.execute(head, scene_state, time_now)

        if self.script.finished():
            print("Script ended", self.script)
            self.script = None

