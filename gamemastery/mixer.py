"""
Entry point for AWS lambda function
"""

import analyzer.mixer.recordings as gmr 
import analyzer.preparation.bouncer as gb
import analyzer.aws.store as AWSStore
import analyzer.aws.queue as AWSQueue
import boto3
import os

def handler(event, context):
    """Download recording info from Mixer.com API and initiate analysis"""

    IS_OFFLINE = os.environ.get('IS_OFFLINE')
    gma_mixer_client_id = os.environ['GMA_MIXER_API_CLIENT_ID']
    gma_mixer_channel_id = os.environ['GMA_MIXER_API_CHANNEL_ID']
    gma_aws_db_table_name = os.environ['GMA_AWS_DB_TABLE_NAME']
    gma_aws_download_queue_name = os.environ['GMA_AWS_DOWNLOAD_QUEUE_NAME']
    #s3_bucket_name = os.environ['MIXER_S3_BUCKET']

    if IS_OFFLINE:
        db = boto3.resource('dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
    else:
        db = boto3.resource('dynamodb')
    s3 = boto3.resource('s3')
    sqs = boto3.resource('sqs')

    recordings = gmr.get_recordings(gma_mixer_client_id, gma_mixer_channel_id)
    b = gb.Bouncer(AWSStore.Store(db, gma_aws_db_table_name), AWSQueue.Queue(sqs.get_queue_by_name(QueueName=gma_aws_download_queue_name)))
    b.check(recordings)
