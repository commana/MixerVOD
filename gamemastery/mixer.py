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

    sqs = boto3.resource('sqs')
    if IS_OFFLINE:
        db = boto3.resource('dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
    else:
        db = boto3.resource('dynamodb')

    bouncer = gb.Bouncer(AWSStore.Store(db, gma_aws_db_table_name))
    
    recordings = gmr.get_recordings(gma_mixer_client_id, gma_mixer_channel_id)
    new_recordings = bouncer.check(recordings)

    # Previous version with direct SQS access
    #queue = AWSQueue.Queue(sqs.get_queue_by_name(QueueName=gma_aws_download_queue_name))
    #queue.enqueue(new_recordings)
    
    # New hls-based version with SNS fanout
    #TODO
    gmr.get_hls_recordings(gma_mixer_client_id, gma_mixer_channel_id)
