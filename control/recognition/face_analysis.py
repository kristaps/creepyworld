
import os
import calendar
import base64
from datetime import datetime

import boto3
from StringIO import StringIO
from botocore.client import Config


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIAJ4BFHTIFGCLP2JKQ')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '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')

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

    return response['FaceDetails']
