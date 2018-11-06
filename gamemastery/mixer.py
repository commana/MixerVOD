import analyzer.mixer.recordings as gmr 
import analyzer.preparation.bouncer as gb
import analyzer.aws.aws_store as gaa
import boto3
import os

def get(event, context):

    db = boto3.resource('dynamodb')
    s3 = boto3.resource('s3')

    mixer_client_id = os.environ['MIXER_API_CLIENT_ID']
    mixer_channel_id = os.environ['MIXER_API_CHANNEL_ID']
    #s3_bucket_name = os.environ['MIXER_S3_BUCKET']

    recordings = gmr.get_recordings(mixer_client_id, mixer_channel_id)
    b = gb.Bouncer(gaa.AWSStore(db, "GameRecordings"), None)
    b.check(recordings)
