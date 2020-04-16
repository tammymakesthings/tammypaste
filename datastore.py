"""
tammypaste: A simple Pastebin-like service with Python, Flask, MongoDB.
Tammy Cravit <tammymakesthings@gmail.com>
Version 1.0, 2020-04-15

File        : datastore.py
Description : Data storage methods for the REST API (api.py). All database
              access is arbitrated through the REST API.
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


import datetime
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError
import yaml


class Datastore:
    """"Datastore class for the tammypaste app.

    Handles all storage of pasties. Currently implemented with a mongodb
    back-end datastroe. The datastore can be created using the create_db.py
    script."""

    def __init__(self, config_path="config.yaml"):
        """Create a new Datastore class.

        The database configuration is read from the file pointed to by the
        config_path parameter."""

        with open(config_path) as cfg_file:
            self._config = yaml.load(cfg_file, Loader=yaml.FullLoader)

        db_config = self._config['database']
        self._client = MongoClient(
            db_config['hostname'],
            db_config['port'],
            username=db_config['api_server']['username'],
            password=db_config['api_server']['password'],
            authSource=db_config['auth_source'],
            authMechanism=db_config['auth_mechanism'])

        self._db = self._client[db_config['db_name']]
        self._pasties = self._db.pasties
        self._counters = self._db.counters

    @property
    def is_connected(self):
        """Check if we're connected to the database."""

        try:
            svr_info = self._client.server_info()
            if svr_info["version"] is not None:
                return True
            return False
        except KeyError:
            return False
        except ServerSelectionTimeoutError:
            return False

    @property
    def connection(self):
        """Get the MongoClient instance representing the database
        connection."""

        return self._client

    @property
    def database(self):
        """Get the mongodb database for the current connection."""

        return self._db

    def get_pasties_count(self):
        """Get the number of pasties in the database."""

        return self._pasties.count_documents({})

    def get_new_pastie_id(self):
        """Increment the next pastie counter and get the new value."""

        res = self._counters.find_one_and_update(
            filter={"counterName": "pasties"},
            update={"$inc": {"counterValue": 1}},
            projection=["counterName", "counterValue"],
            upsert=False,
            return_document=ReturnDocument.AFTER
        )
        return res["counterValue"]

    def get_pastie(self, pastie_id, search_by_unique_id=False):
        """Look up a pastie by its numeric ID or its unique mongo ID."""

        if search_by_unique_id:
            return self._pasties.find_one({"_id": pastie_id})
        return self._pasties.find_one({"id": pastie_id})

    def create_pastie(self, pastie_data):
        """Create a new pastie.

        The pastie_data should be a dictionary with the following keys:

        - id: The new pastie's numeric ID. This can be specified, but normally
          should be None. If the value is None or the key is not present, the
          next numeric ID will be automatically assigned.
        - content: The content of the new pastie.
        - created_at: The timestamp when the pastie was created. If the value
          is None or the key is not present, the current time will be used.
        - updated_at: The timestamp when the pastie was last updated. If the
          value is None  or the key is not present, the current time will be
          used.

        After the pastie is inserted, it is retrieved and returned."""

        if ("id" not in pastie_data) or (pastie_data["id"] is None):
            pastie_data["id"] = self.get_new_pastie_id()

        if "created_at" not in pastie_data:
            pastie_data["created_at"] = str(datetime.datetime.now())
        if pastie_data["created_at"] is None:
            pastie_data["created_at"] = str(datetime.datetime.now())

        if "updated_at" not in pastie_data:
            pastie_data["updated_at"] = str(datetime.datetime.now())
        if pastie_data["updated_at"] is None:
            pastie_data["updated_at"] = str(datetime.datetime.now())

        if self.pastie_exists(int(pastie_data["id"])):
            raise ValueError(f"A pastie with ID {pastie_data['id']} exists")

        new_pastie_id = self._pasties.insert_one(pastie_data)
        return self._pasties.find_one({"_id": new_pastie_id})

    def update_pastie(self, pastie_id, pastie_data):
        """Update a pastie's data. The created_at, updated_at, and content fields
        are the only fields which will be updated. If no pastie with the
        numeric ID pastie_id is found, a KeyError will be raised."""

        rec = self._pasties.find_one({"id": pastie_id})
        if rec is None:
            raise KeyError(f"Pastie with id {pastie_id} not found")
        return self._pasties.replace_one({"id": pastie_id}, {
            "created_at": pastie_data.created_at,
            "updated_at": pastie_data.updated_at,
            "content": pastie_data.content
        })

    def delete_pastie(self, pastie_id):
        """Delete a pastie by its numeric ID."""

        return self._pasties.delete_one({"id": pastie_id})

    def pastie_exists(self, pastie_id):
        """Check if a pastie with the given numeric ID exists."""

        res = self.get_pastie(pastie_id)
        return res is not None

    def list_pasties(self, query=None, max_records=None):
        """Retrieve a list of pasties in the database.

        Optionally, the list can be filtered by passing in a query, and the
        results can be limited to a certain number of records by passing in a
        value for max_records."""
        filt_expr = query or {}
        if max_records is not None:
            return self._pasties.find(filt_expr).limit(max_records).sort("id")
        return self._pasties.find(filt_expr).sort("id")
