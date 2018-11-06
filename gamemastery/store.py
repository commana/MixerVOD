"""
A generic storage interface
"""

class Store(object):
    """Defines the use cases implemented by the underlying storage engine"""

    def filter_known(self, recordings):
        """Returns only those recordings that are not yet listed in the storage table"""
        pass