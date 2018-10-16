import requests
import boto3

# Based on https://stackoverflow.com/a/51758077
url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"
r = requests.get(url, stream=True)

s3 = boto3.resource('s3', region_name='eu-central-1')

bucket_name = 'your-bucket-name'
key_name = 'your-key-name'

bucket = s3.Bucket(bucket_name)
bucket.upload_fileobj(r.raw, key_name)
