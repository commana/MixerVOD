"""
Entry point for AWS lambda function
"""

import analyzer.mixer.recordings as gmr 
import analyzer.preparation.bouncer as gb
import analyzer.aws.aws_store as gaa
import boto3
import os

def handler(event, context):
    """Download recording info from Mixer.com API and initiate analysis"""

    IS_OFFLINE = os.environ.get('IS_OFFLINE')
    mixer_client_id = os.environ['MIXER_API_CLIENT_ID']
    mixer_channel_id = os.environ['MIXER_API_CHANNEL_ID']
    #s3_bucket_name = os.environ['MIXER_S3_BUCKET']

    if IS_OFFLINE:
        db = boto3.resource('dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
    else:
        db = boto3.resource('dynamodb')
    s3 = boto3.resource('s3')

    recordings = gmr.get_recordings(mixer_client_id, mixer_channel_id)
    b = gb.Bouncer(gaa.AWSStore(db, "GameRecordings"), None)
    b.check(recordings)
