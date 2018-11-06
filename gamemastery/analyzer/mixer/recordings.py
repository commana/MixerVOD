"""
Download the list of available recordings of a channel and turn it into generic recording objects.
"""
import requests
import analyzer.preparation.recording as gr

def get_recordings(mixer_client_id, mixer_channel_id):
    s = requests.Session()
    s.headers.update({'Client-ID': mixer_client_id})

    recordings_response = s.get('https://mixer.com/api/v1/recordings?where=channelId:eq:{}'.format(mixer_channel_id))

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
            # TODO: Handle other states (Issue #2)
            continue
        # We assume that all VODs have the same baseUrl
        video_url = rec["vods"][0]["baseUrl"] + "source.mp4"

        # We further assume that the first VOD entry has all information plus it represents the mp4 version!
        data = rec["vods"][0]["data"]
        width = data["width"]
        height = data["height"]
        fps = data["fps"]
        bitrate = data["bitrate"]

        recording_infos.append(gr.Recording({
            "platform": "mixer",
            "id": rec["id"],
            "name": rec["name"],
            "duration": rec["duration"],
            "createdAt": rec["createdAt"],
            "channelId": mixer_channel_id,
            "width": width,
            "height": height,
            "fps": fps,
            "bitrate": bitrate,
            "url": video_url
        }))

    return recording_infos