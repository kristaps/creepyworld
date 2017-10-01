import cv2
import socket
import cv2.bgsegm
import numpy as np
from time import sleep
from threading import Thread
from collections import deque

class Tracker:
    KERNEL_BLUR = (31, 31)
    MIN_CONTOUR_AREA = 500
    WIDTH = 640
    HEIGHT = 480
    #UDP_IP = "192.168.1.55"
    UDP_IP = "192.168.1.104"
    UDP_PORT = 8765

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start_tracking_mog(self):
        #cap = cv2.VideoCapture(1)
        cap = cv2.VideoCapture(0)

        if (not cap.isOpened()):
            print("fuck")

            return

        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

        while True:
            ret, frame = cap.read()

            if frame is not None:
                framecp = frame.copy()

                blur = cv2.GaussianBlur(frame, self.KERNEL_BLUR, 0)

                fgmask = fgbg.apply(frame, learningRate=0.005)

                frame, cont, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                largestcontour, area = self.get_largest_contour(cont)

                if largestcontour is not None:
                    (x, y), radius = cv2.minEnclosingCircle(largestcontour)

                    center = self.get_center(largestcontour)

                    self.coords = self.translate_coords(center)

                    self.send(self.coords[0], self.coords[1])

                    print(str(area))

                    cv2.circle(fgmask, center, 10, (255, 255, 255), -1)
                    cv2.circle(framecp, center, 10, (0, 0, 255), -1)

                cv2.imshow('fgmast', fgmask)
                cv2.imshow('cont', framecp)

                #y1
                #|
                #|
                #|
                #|
                #|
                #|
                #0_______________x1
                    
            k = cv2.waitKey(30) & 0xff

            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def get_center(self):
        if hasattr(self, 'center'):
            return self.center

        return None

    def translate_coords(self, coords):
        new_x = coords[0] / self.WIDTH
        new_y = 1 - (coords[1] / self.HEIGHT)

        return (new_x, new_y)

    def get_largest_contour(self, contours):
        largestcontour = None
        largestarea = self.MIN_CONTOUR_AREA
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largestarea:
                largestcontour = contour
                largestarea = area

        return largestcontour, largestarea

    def get_center(self, contour):
        M = cv2.moments(contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        return (cx, cy)

    def send(self, x, y):
        try:
            message = str(x) + "," + str(y) + "Z"
            self.sock.sendto(message.encode(), (self.UDP_IP, self.UDP_PORT))
            print("sent message:", message)
        except Exception as e:
            print("send exception: ", e)
            self.sock.close()

def main():
    tracker = Tracker()
    tracker.start_tracking_mog()

if __name__ == '__main__':
    main()