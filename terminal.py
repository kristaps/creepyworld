#!/usr/bin/env python

import serial

# Uno
# arduino = serial.Serial('/dev/cu.usbmodemFD121')
# Duemilanove
arduino = serial.Serial('/dev/cu.usbserial-A600etM9')

while True:
    entry = input("Enter command: ")
    arduino.write(entry.encode('ascii'))

