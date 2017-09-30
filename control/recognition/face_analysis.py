
import os
import calendar
import base64
import json
from datetime import datetime

import boto3
from StringIO import StringIO
from botocore.client import Config


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_BUCKET = 'creepyworldfaces'


storage = boto3.resource(
    's3',
    config=Config(signature_version='s3v4'),
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

client = boto3.client(
    'rekognition',
    config=Config(signature_version='s3v4'),
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

CONFIDENCE_THRESHOLD = 80


def extract_face_meta(meta):
    return {
        'Eyeglasses': meta.get('Eyeglasses', {}).get('Value')
        if meta.get('Eyeglasses', {}).get('Confidence') >= CONFIDENCE_THRESHOLD else False,  # True, False
        'Sunglasses': meta.get('Sunglasses', {}).get('Value')
        if meta.get('Sunglasses', {}).get('Confidence') >= CONFIDENCE_THRESHOLD else False,  # True, False
        'Gender': meta.get('Gender', {}).get('Value')
        if meta.get('Gender', {}).get('Confidence') >= CONFIDENCE_THRESHOLD else None,  # 'Male', 'Female', None
        'Mustache': meta.get('Mustache').get('Value')
        if meta.get('Mustache', {}).get('Confidence') >= CONFIDENCE_THRESHOLD else False,  # True, False,
        'AgeRange': meta.get('AgeRange')
    }


# http://boto3.readthedocs.io/en/latest/reference/services/rekognition.html#Rekognition.Client.detect_faces
def analyse_face(image):
    if not isinstance(image, (StringIO, file)):
        raise TypeError('Invalid image types')

    write_key = '{timestamp}-{filename}'.format(
        timestamp=calendar.timegm(datetime.now().utctimetuple()),
        filename=os.path.basename(image.name)
    )

    storage.meta.client.put_object(
        Body=image, Key=write_key,
        Bucket=AWS_BUCKET,
    )

    response = client.detect_faces(
        Image={
            # 'Bytes': base64.b64encode(image_file.read()),
            "S3Object": {
                "Bucket": AWS_BUCKET,
                "Name": write_key
            }
        },
        Attributes=['DEFAULT', 'ALL']
    )

    return map(lambda x: extract_face_meta(x), response['FaceDetails'])


if __name__ == '__main__':
    with open('data/1.jpg') as f:
        print analyse_face(f)
