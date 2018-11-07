"""
Implements the store interface for AWS DynamoDB
"""

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
        print response
        #seen_vods = map(lambda x: x['date'], response['Responses'][self.recording_table_name])
        #process_vods = [x for x in recordings if not str(x['id']) in seen_vods]
        #return process_vods
        return []