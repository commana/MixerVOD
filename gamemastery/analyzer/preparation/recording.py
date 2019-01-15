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

    # See https://stackoverflow.com/a/25176504
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Recording):
            return self.id == other.id and self.platform == other.platform
        return NotImplemented

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))
