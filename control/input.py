import socket
from time import time
from math import sin, cos


class InputController(object):
    x = 0.0
    y = 0.0

    def __init__(self):
        self.position_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.position_socket.bind(('0.0.0.0', 8765))
        self.position_socket.setblocking(False)
        # self.init_time = time()

    def update_input(self, state):
        data = ''
        while True:
            try:
                data += self.position_socket.recv(4096)
            except socket.error as e:
                if e.errno != 35:
                    print("Unexpected socket errno", e.errno)

                break

        messages = data.split('Z')
        while messages:
            last_msg = messages.pop()
            try:
                x, y = last_msg.split(',')
                x = float(x)
                y = float(x)
            except ValueError:
                break

            state.x = x
            state.y = y
            break

        # now = time()
        # state.x = round(sin(now - self.init_time) / 2.0, 4)
        # state.y = round(cos(now - self.init_time) / 2.0, 4)
