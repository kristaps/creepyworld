import socket
from time import time
from math import sin, cos

VISITOR_PRESENCE_SETTLE_TIME = 1.0

class InputController(object):
    x = 0.0
    y = 0.0

    last_position_at = 0.0

    presence_change_at = None

    def __init__(self):
        self.position_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.position_socket.bind(('0.0.0.0', 8765))
        self.position_socket.setblocking(False)

    def update_input(self, state):
        now = time()
        data = str()
        visitor_detected = False

        while True:
            try:
                incoming = self.position_socket.recv(4096)
                data += incoming.decode('ascii')
            except socket.error as e:
                if e.errno != 35:
                    print("Unexpected socket errno", e.errno)

                break

        messages = data.split('Z')
        while messages:
            self.last_position_at = now

            last_msg = messages.pop()
            try:
                x, y = last_msg.split(',')
                x = float(x)
                y = float(x)
                visitor_detected = True
            except ValueError:
                continue

            state.x = x
            state.y = y
            break

        if (state.present != visitor_detected) and (self.presence_change_at is None):
            self.presence_change_at = now
        elif state.present == visitor_detected:
            self.presence_change_at = None

        if self.presence_change_at and now - self.presence_change_at >= VISITOR_PRESENCE_SETTLE_TIME:
            print("Visitor is now", visitor_detected and "present" or "absent")
            state.set_presence(visitor_detected)

        # now = time()
        # state.x = round(sin(now - self.init_time) / 2.0, 4)
        # state.y = round(cos(now - self.init_time) / 2.0, 4)
