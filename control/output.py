import serial
import openal
import os.path
import glob
from .state import NUM_HEADS

COMMAND_FORMAT = "CH{:02d}A{:03d}Z"


def format_angle(angle):
    return "{:3d}".format(angle)

def format_command(index, angle):
    return COMMAND_FORMAT.format(index, angle).encode('ascii')


class OutputController(object):
    last_angles = [format_angle(0) for _ in range(NUM_HEADS)]
    last_audio = [None for _ in range(NUM_HEADS)]

    def __init__(self, device_path):
        print("Initializing serial")
        # self.arduino = serial.Serial(device_path)
        print("Initializing audio")
        self.audio = Audio()
        self.audio.set_listener_position(0.5, 0.5)

    def set_outputs(self, state):
        new_outputs = [
            format_angle(int(round(head.angle_current))) for head in state.heads
        ]

        for index, (old, new) in enumerate(zip(self.last_angles, new_outputs)):
            if old != new:
                self.turn_head(index, new)

        self.last_angles = new_outputs

        for index, (old_audio, head) in enumerate(zip(self.last_audio, state.heads)):
            if old_audio != head.audio_file and head.audio_file is not None:
                self.audio.play(head.audio_file, head.x, head.y)

        self.last_audio = [head.audio_file for head in state.heads]


    def turn_head(self, index, angle):
        angle = int(angle)
        print(format_command(index, angle))
        # self.arduino.write(format_command(index, angle))


class Audio(object):
    sources = {}

    def __init__(self):
        self.load_files()
        self.listener = openal.oalGetListener()

    def load_files(self):
        for path in glob.glob(os.path.dirname(__file__) + '/../media/*'):
            filename = os.path.split(path)[-1]
            print("Loading", filename)
            self.sources[filename] = openal.oalOpen(path)

    def play(self, file, x, y):
        print("Playing", file, x, y)
        if file in self.sources:
            source = self.sources[file]
            # x = {0.1: -9.5, 0.5: 0.5, 0.9: 10.5}[x]
            # y = {0.1: -9.5, 0.5: 0.5, 0.9: 10.5}[y]
            print (x, y)
            source.set_position((x, y, 0.0))
            source.play()

    def set_listener_position(self, x, y):
        self.listener.set_position((x, y, 0.0))
