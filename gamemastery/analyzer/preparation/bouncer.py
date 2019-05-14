"""
Let's in only new recordings
"""

class Bouncer(object):
    """Receives a list of recordings and decides if they may proceed to the next phase."""

    def __init__(self, store):
        self.store = store

    def check(self, recordings):
        new_recordings = self.store.filter_known(recordings)
        self.store.remember(new_recordings)
        return new_recordings
