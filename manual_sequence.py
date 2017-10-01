#!/usr/bin/env python

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

steps = [
    'AudioTest',
    'AudioTest',
]

while steps:
    next_step = steps.pop(0)
    input("Press enter to execute {}".format(next_step))
    sock.sendto(bytes(next_step + '\n', 'ascii'), ('127.0.0.1', 9999))
