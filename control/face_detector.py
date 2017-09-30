import cv2
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

    def __init__(self):
        pass

    def start_tracking_mog(self):
        cap = cv2.VideoCapture(1)

        if (not cap.isOpened()):
            print("fuck")

            return

        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

        while True:
            ret, frame = cap.read()

            if frame is not None:
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                cv2.imshow('img',frame)

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

def main():
    tracker = Tracker()
    tracker.start_tracking_mog()

if __name__ == '__main__':
    main()