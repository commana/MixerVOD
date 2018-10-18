import requests
import boto3
from slugify import slugify

# Based on https://stackoverflow.com/a/51758077
def upload_recording(bucket, vod, callback):
    r = requests.get(vod["url"], stream=True)
    total_length = r.headers.get('content-length')

    key_name = "{}-{}-{}".format(vod["id"], vod["createdAt"], vod["name"])
    bucket.upload_fileobj(r.raw, slugify(key_name), Callback=lambda x: callback(total_length, x))
