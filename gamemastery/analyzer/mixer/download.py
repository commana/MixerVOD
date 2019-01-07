import StringIO
import requests
import boto3
import json
import os
import io

max_size_in_gb = 4 * 1024 * 1024 * 1024
GMA_AWS_BUCKET_NAME = os.environ['GMA_AWS_BUCKET_NAME']
s3r = boto3.resource('s3')
bucket = s3r.Bucket(GMA_AWS_BUCKET_NAME)
s3 = boto3.client('s3')

# See https://stackoverflow.com/a/26853961
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

event = {}
event['id'] = "DEADBEEF"
event['url'] = "https://vodcontent-2008.xboxlive.com/channel-47094669-public/918ff7e8-13af-43ba-9f92-88574919408c/source.mp4"

def get_download_size(event, context):
    """
    Get the size of the video file
    """
    r = requests.head(event['url'])
    size = r.headers['Content-Length']
    return json.dumps(merge_two_dicts(event, {
        "size": size,
        "completed_size": 0,
    }))

def initiate_multipart_upload(event, context):
    mpu = s3.create_multipart_upload(Bucket=GMA_AWS_BUCKET_NAME, Key=event['id'])
    return json.dumps(merge_two_dicts(event, {
        "upload_id": mpu['UploadId']
    }))

def upload_part(event, context):
    part_file = "/tmp/{}_{}_{}.mp4".format(event['id'], event['upload_id'], event['part_no'])
    headers = {"Range": "bytes={:d}-{:d}".format(event['range_start'], event['range_end'])}

    r = requests.get(event["url"], headers=headers, stream=True)
    with open(part_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    with io.open(part_file, mode='rb') as f:
        response = s3.upload_part(Body=f, Bucket=GMA_AWS_BUCKET_NAME, Key=event['id'], UploadId=event['upload_id'], PartNumber=event['part_no'])
    return json.dumps(merge_two_dicts(event, {
        "part_etag": response['ETag'],
        "completed_size": (event['range_end'] - event['range_start'])
    }))

def complete_upload(event, context):
    pass

def abort_upload(event, context):
    mpu = s3.MultipartUpload(GMA_AWS_BUCKET_NAME, generate_name(event), event['id'])
    response = mpu.abort()
    return json.dumps({
        "recording": event.recording,
        "size": event.size,
        "upload_id": mpu.upload_id,
        "abort_response": response
    })

def finalize_recording(event, context):
    """
    Mark download as complete so that the analyzer can start its work
    """
    # Mark as downloaded in DynamoDB
    # Store recording in SQS
    pass

def generate_name(event):
    return "mixer_{}.mp4".format(event['id'])




event2 = json.loads(get_download_size(event, None))
if int(event2['size']) > max_size_in_gb:
    raise Exception("VOD has {} bytes, a maximum of {} is allowed".format(event2['size'], max_size_in_gb))
event3 = json.loads(initiate_multipart_upload(event2, None))
event3['part_no'] = 1
event3['range_start'] = 0
event3['range_end'] = 5 * 1024 * 1024
event4 = json.loads(upload_part(event3, None))
print event4