
import os
import time
import base64
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

CONFIDENCE_THRESHOLD = 60


# http://boto3.readthedocs.io/en/latest/reference/services/rekognition.html#Rekognition.Client.detect_faces
def analyse_face(image):
    if not isinstance(image, (StringIO, file)):
        raise TypeError('Invalid image types')

    write_key = '{timestamp}-{filename}'.format(
        timestamp=time.mktime(datetime.now().timetuple()),
        filename=image.name
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

    return response['FaceDetails']


if __name__ == '__main__':
    with open('data/1.jpg', 'r') as image_file:
        print analyse_face(image_file)