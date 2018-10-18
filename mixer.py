import boto3
import os, sys
import vod_list
import vod_selector
import vod_upload

db = boto3.resource('dynamodb', region_name='eu-central-1', endpoint_url="http://localhost:8000")
s3 = boto3.resource('s3', region_name='eu-central-1')

mixer_client_id = os.environ['MIXER_API_CLIENT_ID']
mixer_channel_id = os.environ['MIXER_API_CHANNEL_ID']
s3_bucket_name = os.environ['MIXER_S3_BUCKET']

recordings = vod_list.get_recordings(mixer_client_id, mixer_channel_id)
recordings_to_process = vod_selector.filter_recordings(db, recordings)

def progress(total_length, current_length):
    sys.stdout.write("\rCurrent progress: {}%".format(float(current_length)/total_length))
    sys.stdout.flush()

bucket = s3.Bucket(s3_bucket_name)
for vod in recordings_to_process:
    print "Processing '{}' created at {}...".format(vod["name"], vod["createdAt"])
    vod_upload.upload_recording(bucket, vod, progress)
