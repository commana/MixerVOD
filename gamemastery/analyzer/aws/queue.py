"""
Implements the queue interface for AWS SQS
"""

class Queue(object):
    """Defines the use cases implemented by the underlying queue"""

    def __init__(self, sqs):
        self.sqs = sqs
    
    def enqueue(self, recordings):
        """Send all recordings to the queue"""
        pass