import requests
import sys
import datetime

"""
Extract all available recordings by date
"""

s = requests.Session()
s.headers.update({'Client-ID': '21c05a70d3ad447497efda7723a429cfc0da4cbd721cfaae'})

channel_response = s.get('https://mixer.com/api/v1/recordings?where=channelId:eq:47094669')

# All recordings available on the channel
# Key properties:
#   - createdAt
#   - state == AVAILABLE
#   - name
#   - vods[] - baseUrl - source.mp4
recordings = channel_response.json()

recording_infos = []
for rec in recordings:
    if not rec["state"] == "AVAILABLE":
        continue
    video_url = rec["vods"][0]["baseUrl"] + "source.mp4"

    id = rec["id"]
    name = rec["name"]
    createdAt = rec["createdAt"]
    # The seconds part and the timezone identifier are hard coded, this could fail at some point
    createdAtDate = datetime.datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%S.000Z")
    recording_infos.append({"id":id, "createdAt":createdAtDate})

print sorted(recording_infos, key=lambda rec: rec["createdAt"])
