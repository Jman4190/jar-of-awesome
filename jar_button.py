# updated on 2019-01-28
import twilio
from twilio.rest import Client
import random
import boto3
import os
from dotenv import load_dotenv
load_dotenv()

# Your Account Sid and Auth Token from twilio.com/console
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
TO_NUMBER = os.getenv('TO_NUMBER')
FROM_NUMBER = os.getenv('FROM_NUMBER')

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# connect to AWS S3 
s3 = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key= AWS_SECRET_ACCESS_KEY)

def lambda_handler(event, context):
    # update with new file names here after adding them to s3 bucket

    # function to get s3 keys
    def get_s3_keys(bucket):
    """Get a list of keys in an S3 bucket."""
        keys = []
        resp = s3.list_objects_v2(Bucket=bucket)
        for obj in resp['Contents']:

            keys.append(obj['Key'])
        return keys

    # get list of keys
    images = get_s3_keys('memoryjarphotos')
    # pick random file from keys
    key = random.choice(images)
    # save file to url
    media = ('https://s3-us-west-1.amazonaws.com/memoryjarphotos/{}'.format(key))

    # send MMS
    client.messages.create(
        to=TO_NUMBER,
        from_=FROM_NUMBER,
        body="Thanks for reaching in the Jar of Awesome!",
        media_url=media)

    print('Done!')
