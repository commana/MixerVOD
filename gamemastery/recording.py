"""
Meta-data about a recording
"""

class Recording(object):
    """A generic recording object"""

    def __init__(self, data_dict):
        self.platform = data_dict['platform']
        self.id = data_dict['id']
        self.name = data_dict['name']
        self.duration = data_dict['duration']
        self.createdAt = data_dict['createdAt']
        self.channelId = data_dict['channelId']
        self.width = data_dict['width']
        self.height = data_dict['height']
        self.fps = data_dict['fps']
        self.bitrate = data_dict['bitrate']
        self.url = data_dict['url']