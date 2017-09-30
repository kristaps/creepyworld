from time import time
from .state import SceneState, InputState
from .input import InputController
from .output import OutputController
from .director import Director


def main():
    input_controller = InputController()
    output_controller = OutputController()

    input_state = InputState()
    scene_state = SceneState()

    director = Director()

    while True:
        now = time()
        input_controller.update_input(input_state)
        director.direct(now, scene_state, input_state)
        scene_state.update(now)
        output_controller.set_outputs(scene_state)


if __name__ == '__main__':
    main()