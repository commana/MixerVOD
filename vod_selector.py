import json
import boto3

"""
Example JSON accepted by this script:
[{
    "url": "<url to source.mp4>",
    "id": 58466226,
    "createdAt": "2018-10-03T14:56:42.000Z",
    "name": "[XB1S] Wednesday Hype"
}]
"""

# TODO: Remove testing code
input = "json"
f = open("vods.json", "r")
input = json.load(f)
f.close()

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', endpoint_url="http://localhost:8000")

def check_ids(db, vods):
    ids = []
    for vod in vods:
        ids.append({'date': str(vod["id"])})
    # check database
    response = dynamodb.batch_get_item(RequestItems={
        'last_seen_recording': {'Keys': ids}
    })
    return map(lambda x: x['date'], response['Responses']['last_seen_recording'])

def mark_ids(db, vods):
    if len(vods) == 0:
        return
    put_items = []
    for vod in vods:
        put_items.append({'PutRequest': {'Item': {'date': str(vod['id'])}}})

    dynamodb.batch_write_item(RequestItems={
        'last_seen_recording': put_items
    })

seen_vods = check_ids(dynamodb, input)
process_vods = [x for x in input if not str(x['id']) in seen_vods]

mark_ids(dynamodb, process_vods)

print json.dumps(process_vods)