"""json append from dynamodb."""
import boto3
import json
import os
# bucket
BUCKET = os.getenv('BUCKET_NAME', 'test-qrcode')

# s3
S3 = boto3.resource('s3')
S3CLIENT = boto3.client('s3')
BUCKET_DATA = S3.Bucket(BUCKET)

JSON_FILENAME = os.getenv('JSON_FILENAME', 'data.json')


class base(object):
    """base class."""

    def __init__(self, **kwargs):
        """Initialize setting."""
        self.params = kwargs

    def get_json(self):
        """Get json file from s3."""
        self.obj = BUCKET_DATA.Object(JSON_FILENAME)
        response = self.obj.get()
        body = response['Body'].read()
        self.json_data = json.loads(body.decode('utf-8'))

    def append_data_to_json(self):
        """Add parameters to json."""
        self.json_data.append(self.params)
        print(self.json_data)

    def update_json_s3(self):
        """Update json file on S3."""
        self.obj.put(
            Body=json.dumps(self.json_data),
            ContentType='application/json'
        )


def lambda_handler(event, context):
    """main."""
    print(event['Records'][0]['dynamodb']['NewImage'])
    add_data = event['Records'][0]['dynamodb']['NewImage']
    username = add_data['id']['S']
    request_time_unix = 1531157063
    count = 1
    csv = "1531246040338/QRcode_uri_3a9e7f402665e249.csv"

    test = base(
        username=username,
        request_time_unix=request_time_unix,
        count=count,
        csv=csv
    )
    test.get_json()
    test.append_data_to_json()
    # test.update_json_s3()


event = {'Records': [{'eventID': '150fe8e8e674f858fd3332c274368eaa', 'eventName': 'INSERT', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'ap-northeast-1', 'dynamodb': {'ApproximateCreationDateTime': 1531387980.0, 'Keys': {'id': {'S': 'huga'}},
                                                                                                                                                                                              'NewImage': {'id': {'S': 'huga'}}, 'SequenceNumber': '200000000013957125378', 'SizeBytes': 12, 'StreamViewType': 'NEW_IMAGE'}, 'eventSourceARN': 'arn:aws:dynamodb:ap-northeast-1:438704618616:table/test-stream-DynamoDBTable-M2BCW0WLK8VX/stream/2018-07-12T08:43:09.669'}]}
lambda_handler(event, None)
