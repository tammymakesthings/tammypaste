import unittest
from datastore import Datastore


class TestAPI(unittest.TestCase):
    """Tests for the API service."""

    def setUp(self):
        self.datastore = Datastore()
