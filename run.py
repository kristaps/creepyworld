#!/usr/bin/env python

from time import time, sleep
from control.state import SceneState, InputState
from control.input import InputController
from control.output import OutputController
from control.director import Director
from control import scripts


# SERIAL_DEVICE = '/dev/cu.usbserial-A600etM9'
SERIAL_DEVICE = '/dev/cu.usbmodemFD121'
# SERIAL_DEVICE = '/dev/cu.usbmodemFA131'

FRAME_TIME = 1.0 / 1.0

def main():
    input_controller = InputController()
    output_controller = OutputController(SERIAL_DEVICE)

    input_state = InputState()
    scene_state = SceneState()

    now = time()
    director = Director(now)

    print("Entering main loop")
    while True:
        now = time()
        input_controller.update_input(input_state)

        if input_state.run_script:
            script_class = getattr(scripts, input_state.run_script, None)
            if script_class:
                director.start_script(script_class(), now)
            input_state.run_script = None

        director.direct(now, scene_state, input_state)
        scene_state.update(now)
        output_controller.set_outputs(scene_state)

        sleep(max(0.0, now + FRAME_TIME - time()))


if __name__ == '__main__':
    main()
