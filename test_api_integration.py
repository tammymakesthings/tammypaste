"""
tammypaste: A simple Pastebin-like service with Python, Flask, MongoDB.
Tammy Cravit <tammymakesthings@gmail.com>
Version 1.0, 2020-04-15

File        : test_api.py
Description : Unit tests for the REST API (ihntegration)
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
import requests

from datastore import Datastore


class TestAPI(unittest.TestCase):
    """Tests for the API service (ihntegration unit tests)."""

    def setUp(self):
        self.datastore = Datastore()
