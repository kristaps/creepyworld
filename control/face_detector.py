import cv2
import cv2.bgsegm
import numpy as np
from time import sleep
from threading import Thread
from collections import deque
import calendar
import base64
import json
from datetime import datetime
import os.path
import boto3
from botocore.client import Config

class Tracker:
    KERNEL_BLUR = (31, 31)
    MIN_CONTOUR_AREA = 500
    WIDTH = 640
    HEIGHT = 480
    SENT = False

    def __init__(self):
        pass

    def start_tracking_mog(self):
        cap = cv2.VideoCapture(1)

        if (not cap.isOpened()):
            print("fuck")

            return

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        while True:
            ret, frame = cap.read()

            if frame is not None:
                framecp = frame.copy()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]


                cv2.imshow('img', frame)

                if len(faces) > 0 and not self.SENT:
                    cv2.imwrite('test.png', framecp)
                    with open('test.png', 'rb') as f:
                        self.face_metas = self.analyse_face(f)
                        print(self.face_metas)
                        #self.SENT = True

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

        import os



    AWS_ACCESS_KEY_ID = 'AKIAJQRJAAIWPYSPN2MQ'
    AWS_SECRET_ACCESS_KEY = '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'

    AWS_BUCKET = 'creepyworldfaces'

    storage = boto3.resource(
        's3',
        config=Config(signature_version='s3v4'),
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )

    client = boto3.client(
        'rekognition',
        config=Config(signature_version='s3v4'),
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )

    def extract_face_meta(self, meta):
        return {
            'Eyeglasses': meta.get('Eyeglasses', {}).get('Value')
            if meta.get('Eyeglasses', {}).get('Confidence') >= 80 else False,  # True, False
            'Sunglasses': meta.get('Sunglasses', {}).get('Value')
            if meta.get('Sunglasses', {}).get('Confidence') >= 80 else False,  # True, False
            'Gender': meta.get('Gender', {}).get('Value')
            if meta.get('Gender', {}).get('Confidence') >= 80 else None,  # 'Male', 'Female', None
            'Mustache': meta.get('Mustache').get('Value')
            if meta.get('Mustache', {}).get('Confidence') >= 80 else False,  # True, False,
            'AgeRange': meta.get('AgeRange')
    }


    # http://boto3.readthedocs.io/en/latest/reference/services/rekognition.html#Rekognition.Client.detect_faces
    def analyse_face(self, image):
        write_key = '{timestamp}-{filename}'.format(
            timestamp=calendar.timegm(datetime.now().utctimetuple()),
            filename=os.path.basename(image.name)
        )

        self.storage.meta.client.put_object(
            Body=image, Key=write_key,
            Bucket=self.AWS_BUCKET,
        )

        response = self.client.detect_faces(
            Image={
            # 'Bytes': base64.b64encode(image_file.read()),
                "S3Object": {
                    "Bucket": self.AWS_BUCKET,
                    "Name": write_key
                }
            },
            Attributes=['DEFAULT', 'ALL']
        )

        return list(map(lambda x: self.extract_face_meta(x), response['FaceDetails']))

def main():
        tracker = Tracker()
        tracker.start_tracking_mog()

if __name__ == '__main__':
    main()