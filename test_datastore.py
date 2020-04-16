import unittest
from datastore import Datastore


class TestDataStore(unittest.TestCase):
    """Tests for the Datastore class."""

    def setUp(self):
        self.datastore = Datastore()

    def test_can_connect_to_db(self):
        """Verify that we can connect to the database."""
        self.assertTrue(self.datastore.is_connected)

    def test_can_get_pastie_count(self):
        """Test that we can get the pastie count and it's a number."""
        try:
            pastie_count = int(self.datastore.get_pasties_count())
        except ValueError:
            self.fail("get_pasties_count() returned something non-numeric")
        self.assertIsNotNone(pastie_count)

    def test_can_look_up_pasties(self):
        "Verify that get_pastie works."
        test_record = self.datastore.get_pastie(1)
        self.assertIsNotNone(test_record)
        self.assertEqual(test_record["id"], 1)

    def test_look_up_undefined_pastie_returns_none(self):
        test_record = self.datastore.get_pastie(0)
        self.assertIsNone(test_record)

    def test_can_create_pasties(self):
        pass

    def test_new_pasties_fill_in_missing_id(self):
        pass

    def test_new_pasties_fill_in_missing_created_at(self):
        pass

    def test_new_pasties_fill_in_missing_updated_at(self):
        pass

    def test_create_pastie_with_duplicate_id_throws_error(self):
        pass

    

if __name__ == "__main__":
    unittest.main()
