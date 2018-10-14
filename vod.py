import requests
import json
import os

"""
Extract all available recordings by date
"""

client_id = os.environ['MIXER_API_CLIENT_ID']
channel_id = os.environ['MIXER_API_CHANNEL_ID']

s = requests.Session()
s.headers.update({'Client-ID': client_id})

recordings_response = s.get('https://mixer.com/api/v1/recordings?where=channelId:eq:{}'.format(channel_id))

# All recordings available on the channel
# Key properties:
#   - createdAt
#   - state == AVAILABLE
#   - name
#   - vods[] - baseUrl - source.mp4
recordings = recordings_response.json()

recording_infos = []
for rec in recordings:
    if not rec["state"] == "AVAILABLE":
        continue
    # We assume that all VODs have the same baseUrl
    video_url = rec["vods"][0]["baseUrl"] + "source.mp4"

    id = rec["id"]
    name = rec["name"]
    createdAt = rec["createdAt"]
    recording_infos.append({"id":id, "name":name, "createdAt":createdAt, "url":video_url})

sorted_recordings = sorted(recording_infos, key=lambda rec: rec["createdAt"])

# We now have a list of recordings, sorted by date.
# We export the list as JSON to be picked up by the next script.

print json.dumps(sorted_recordings)
