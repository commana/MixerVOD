"""
Transforms a regular Recording object into a format suitable for DynamoDB.
"""

import analyzer.preparation.recording as recording
import decimal as dec
import copy

class DBRecording(object):

    def to_dynamodb(self, obj):
        clone = copy.copy(obj)
        clone.fps = self.to_decimal(clone.fps)
        clone.duration = self.to_decimal(clone.duration)
        # Table keys
        clone.Channel = self.get_channel(clone)
        clone.Recording = clone.id
        return clone

    def from_dynamodb(self, obj):
        clone = copy.copy(obj)
        clone.fps = self.from_decimal(clone.fps)
        clone.duration = self.from_decimal(clone.duration)
        # Table keys
        del clone.Channel
        del clone.Recording
        return clone

    def get_channel(self, obj):
        return "{}:{}".format(obj.platform, obj.channelId)

    def to_decimal(self, value):
        return dec.Decimal(str(value))
    
    def from_decimal(self, value):
        return float(value)