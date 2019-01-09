import StringIO
import requests
import boto3
import json
import os
import io

max_size_in_gb = 4 * 1024 * 1024 * 1024
RANGE_SIZE = 500 * 1024 * 1024 # KEEP IN SYNC WITH STEP FUNCTION
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

def get_recording_size(event, context):
    """
    Get the size of the video file
    """
    r = requests.head(event['url'])
    size = int(r.headers['Content-Length'])
    return merge_two_dicts(event, {
        "size": size,
        "is_completed": False
    })

def initiate_multipart_upload(event, context):
    mpu = s3.create_multipart_upload(Bucket=GMA_AWS_BUCKET_NAME, Key=event['id'])
    return merge_two_dicts(event, {
        "upload_id": mpu['UploadId'],
        "part_base_no": 0,
        "completed_parts": []
    })

def upload_part(event, context):
    """
    Upload one part of a video file to S3
    """
    # Compute parameters
    part_no = event['number'] + event['part_base_no']
    range_start = (part_no - 1) * RANGE_SIZE
    range_end = range_start + RANGE_SIZE - 1

    part_file = "/tmp/{}_{}_{}.mp4".format(event['id'], event['upload_id'], part_no)
    headers = {"Range": "bytes={:d}-{:d}".format(range_start, range_end)}

    r = requests.get(event["url"], headers=headers, stream=True)
    with open(part_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    response = {}
    with io.open(part_file, mode='rb') as f:
        response = s3.upload_part(Body=f, Bucket=GMA_AWS_BUCKET_NAME, Key=event['id'], UploadId=event['upload_id'], PartNumber=part_no)

    os.unlink(part_file)

    return merge_two_dicts(event, {
        "part": {
            # This uses S3 specific namings
            "ETag": response['ETag'],
            "PartNumber": part_no
        }
    })

def merge_partial_uploads(event, context):
    """
    Combine information from the parallel exection of multiple upload_part functions.
    """
    # Event is an array containing all results from parallel execution. They all contain the same
    # information except for 'part', which is the actual result from each parallel job.
    result = None
    for p in event:
        if not result:
            result = p.copy()
            del result['part']
            del result['number']
        result['completed_parts'].append(p['part'])

    completed_size = len(result['completed_parts']) * RANGE_SIZE
    result['is_completed'] = completed_size >= result['size']
    result['part_base_no'] = len(result['completed_parts'])
    return result

def complete_upload(event, context):
    """
    Complete a multi-part upload
    """
    part_info = {
        'Parts': event['completed_parts']
    }
    s3.complete_multipart_upload(Bucket=GMA_AWS_BUCKET_NAME, Key=event['id'], UploadId=event['upload_id'], MultipartUpload=part_info)
    del event['completed_parts']
    return event

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




event2 = get_recording_size(event, None)
if int(event2['size']) > max_size_in_gb:
    raise Exception("VOD has {} bytes, a maximum of {} is allowed".format(event2['size'], max_size_in_gb))
event3 = initiate_multipart_upload(event2, None)
while event3['is_completed'] == False:
    event3['number'] = 1
    eventX = upload_part(event3, None)
    event3 = merge_partial_uploads([eventX], None)
event4 = complete_upload(event3, None)