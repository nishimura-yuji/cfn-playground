import boto3
import json
import os
# bucket
BUCKET = os.getenv('BUCKET_NAME', 'lixilqrcode')

# s3
S3 = boto3.resource('s3')
S3CLIENT = boto3.client('s3')
BUCKET_DATA = S3.Bucket(BUCKET)

JSON_FILENAME = 'data.json'


class base(object):
    """base class."""

    def __init__(self, **kwargs):
        """Initialize setting."""
        self.username = kwargs['username']
        self.request_time_unix = kwargs['request_time_unix']
        self.count = kwargs['count']
        self.csv = kwargs['csv']
        self.params = {
            "username": self.username,
            "request_time_unix": self.request_time_unix,
            "count": self.count,
            "csv": self.csv
        }

    def get_db_data(self):
        """Get json file from s3."""
        BUCKET_DATA.download_file(JSON_FILENAME, '/tmp/' + JSON_FILENAME)
        obj = S3.Object(BUCKET, JSON_FILENAME)
        response = obj.get()
        body = response['Body'].read()

        print(type(body))
        # => <class 'bytes'>

        print(body.decode('utf-8'))

    def append_json(self):
        """Add parameters to json."""


def lambda_handler(event, context):
    """main."""
    print(event['Records'])


event = {'Records': [{'eventID': '150fe8e8e674f858fd3332c274368eaa', 'eventName': 'INSERT', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'ap-northeast-1', 'dynamodb': {'ApproximateCreationDateTime': 1531387980.0, 'Keys': {'id': {'S': 'huga'}},
                                                                                                                                                                                              'NewImage': {'id': {'S': 'huga'}}, 'SequenceNumber': '200000000013957125378', 'SizeBytes': 12, 'StreamViewType': 'NEW_IMAGE'}, 'eventSourceARN': 'arn:aws:dynamodb:ap-northeast-1:438704618616:table/test-stream-DynamoDBTable-M2BCW0WLK8VX/stream/2018-07-12T08:43:09.669'}]}
lambda_handler(event, None)
