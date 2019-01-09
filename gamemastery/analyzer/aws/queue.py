"""
Implements the queue interface for AWS SQS
"""

import json

class Queue(object):
    """Defines the use cases implemented by the underlying queue"""

    def __init__(self, sqs):
        self.sqs = sqs
    
    def enqueue(self, recordings):
        """Send all recordings to the queue"""
        recs = recordings
        # Whe can batch-send at most 10 items to the queue
        while len(recs) > 0:
            batch_recordings = recs[0:9]
            response = self.sqs.send_messages(Entries=batch_recordings)
            print(response.get('Failed'))
            recs = recs[10:]