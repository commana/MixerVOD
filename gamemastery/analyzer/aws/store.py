"""
Implements the store interface for AWS DynamoDB
"""

from analyzer.preparation import recording
import analyzer.aws.db_recording as dbrec

class Store(object):
    """Defines the use cases implemented by the underlying storage engine"""

    def __init__(self, dynamodb, recording_table_name):
        self.db = dynamodb
        self.recording_table_name = recording_table_name

    def filter_known(self, recordings):
        """Returns only those recordings that are not yet listed in the storage table"""
        ids = []
        for rec in recordings:
            ids.append({
                "Channel": "{}:{}".format(rec.platform, rec.channelId),
                "Recording": rec.id
            })
        
        # check database
        rqs = {}
        rqs[self.recording_table_name] = {'Keys': ids}
        response = self.db.batch_get_item(RequestItems=rqs)
        seen_recordings = map(lambda x: recording.Recording(x), response['Responses'][self.recording_table_name])
        new_recordings = [x for x in recordings if not x in seen_recordings]
        return new_recordings

    def remember(self, recordings):
        if len(recordings) == 0:
            return

        put_items = []
        for recording in recordings:
            put_items.append({'PutRequest': {'Item': vars(dbrec.DBRecording().to_dynamodb(recording))}})

        self.db.batch_write_item(RequestItems={
            self.recording_table_name: put_items
        })
