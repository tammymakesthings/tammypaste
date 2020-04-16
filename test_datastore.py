"""
tammypaste: A simple Pastebin-like service with Python, Flask, MongoDB.
Tammy Cravit <tammymakesthings@gmail.com>
Version 1.0, 2020-04-15

File        : test_datastore.py
Description : Unit tests for the datastore object.
==============================================================================
Copyright 2020 Tammy Cravit <tammymakesthings@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

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
        """Make sure we get None back when we look up a nonexistent pastie."""
        test_record = self.datastore.get_pastie(0)
        self.assertIsNone(test_record)

    def test_can_create_pasties(self):
        """Verify that we can create a new pastie."""
        pass

    def test_new_pasties_fill_in_missing_attrs(self):
        """Check that missing attributes are filled in on creation."""
        pass

    def test_create_pastie_with_duplicate_id_throws_error(self):
        """Check that creation enforces unique ids"""
        pass

    def test_update_pastie(self):
        """Verify that we can update a pastie."""
        pass

    def test_update_does_not_change_id(self):
        """Verify that the ID field is immutable once created."""
        pass

    def test_delete_pastie(self):
        """Verify that we can delete a pastie"""
        pass

    def test_delete_invalid_pastie_returns_error(self):
        """Verify that we get an error on deleting an invalid pastie ID"""
        pass

    def test_pastie_exists(self):
        """Verify that the pastie_exists method works"""
        pass

    def test_list_pasties(self):
        """Verify that list_pasties works"""
        pass

    def test_list_pasties_with_filter(self):
        """Verify that list_pasties works with a filter expression"""
        pass

    def test_list_pasties_with_limit(self):
        """Verify that list_pasties works with a limit value"""
        pass

    def test_list_pasties_with_filter_and_limit(self):
        """Verify that list_pasties works with a limit and filter"""
        pass


if __name__ == "__main__":
    unittest.main()
