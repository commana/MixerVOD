import json

"""
Example JSON accepted by this script:
[{
    "url": "<url to source.mp4>",
    "id": 58466226,
    "createdAt": "2018-10-03T14:56:42.000Z",
    "name": "[XB1S] Wednesday Hype"
}]
"""

def filter_recordings(dynamodb, input):
    def db_get_ids(vods):
        ids = []
        for vod in vods:
            ids.append({'date': str(vod["id"])})
        # check database
        response = dynamodb.batch_get_item(RequestItems={
            'last_seen_recording': {'Keys': ids}
        })
        return map(lambda x: x['date'], response['Responses']['last_seen_recording'])

    def db_store_ids(vods):
        if len(vods) == 0:
            return
        put_items = []
        for vod in vods:
            put_items.append({'PutRequest': {'Item': {'date': str(vod['id'])}}})

        dynamodb.batch_write_item(RequestItems={
            'last_seen_recording': put_items
        })

    seen_vods = db_get_ids(input)
    process_vods = [x for x in input if not str(x['id']) in seen_vods]

    db_store_ids(process_vods)

    return process_vods
