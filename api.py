#!python
"""
tammypaste: A simple Pastebin-like service with Python, Flask, MongoDB.
Tammy Cravit <tammymakesthings@gmail.com>
Version 1.0, 2020-04-15

File        : api.py
Description : Application REST API. All database access is arbitrated through
              the REST API.
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

import yaml

from flask import Flask, jsonify, make_response, request, url_for, abort
import flask_httpauth
from flask_httpauth import HTTPBasicAuth
from datastore import Datastore

API_SERVER_VERSION = "0.0.1"
LISTEN_PORT = 5000

api_app = Flask(__name__)     # pylint disable=invalid-name
http_auth = HTTPBasicAuth()   # pylint disable=invalid-name
app_users = {}                # pylint disable=invalid-name
db = Datastore()              # pylint disable=invalid-name

#############################################################################
# Error handlers
#############################################################################


@api_app.errorhandler(404)
def not_found(error):
    """Error handler for 404 (pastie not found) errors."""
    return make_response(jsonify({'error': 'Not Found', 'details': error}),
                         404)


#############################################################################
# Helper methods
#############################################################################

def read_userdb(filename="users.yaml"):
    """Read the API userlist from the YAML file."""
    with open(filename) as user_file:
        userlist = yaml.load(user_file, Loader=yaml.FullLoader)
    return userlist


def validate_user_token(username, token):
    """Validate an API user exists and has the correct token."""
    try:
        if app_users[username] == token:
            return True
    except KeyError:
        return False
    return False


def get_next_pastie_id():
    """Get the next pastie ID for insertion."""
    return db.get_new_pastie_id()


def get_pastie_by_id(pastie_id):
    """Get a pastie by ID if it exists. Returns None if not."""
    return db.get_pastie(pastie_id)


def make_public_pastie(pastie):
    """Add a URL field to a pastie for public use."""
    new_pastie_data = {}
    for field in pastie:
        if field == 'id':
            new_pastie_data['id'] = pastie['id']
            new_pastie_data['url'] = url_for('get_pastie',
                                             pastie_id=pastie['id'],
                                             _external=True)
        else:
            new_pastie_data[field] = pastie[field]
    return new_pastie_data


#############################################################################
# Authentication Methods
#############################################################################

@http_auth.get_password
def get_password(username):
    """Return the password (API token) for a specified user. If the user does
    not exist, returns None."""
    if username in app_users.keys():
        return app_users[username]
    return None


@http_auth.error_handler
def unauthorized():
    """Return an HTTP 401 error if the user is unauthorized."""
    return make_response(jsonify({'error': 'Unauthorized'}), 401)


#############################################################################
# API methods
#############################################################################


@api_app.route('/api/pasties', methods=['GET'])
@http_auth.login_required
def get_pasties():
    """Return a list of the defined pasties."""
    pasties = db.list_pasties(None)
    return jsonify({'pasties': [make_public_pastie(p) for p in pasties]})


@api_app.route('/api/pasties/<int:pastie_id>', methods=['GET'])
@http_auth.login_required
def get_pastie(pastie_id):
    """Return a specific pastie by numeric ID. Returns an HTTP 404 error if
    the requested pastie does not exist."""
    pastie = get_pastie_by_id(pastie_id)
    if pastie is None:
        abort(404)
    return jsonify({'pastie': make_public_pastie(pastie)})


@api_app.route('/api/pastie', methods=['POST'])
@http_auth.login_required
def new_pastie():
    """Create a new pastie and save it. Returns the newly created pastie with
    its ID and URL properties set."""
    if not request.json or 'content' not in request.json:
        abort(400)
    pastie = {
        'content': request.json.get('content', '')
    }
    the_pastie = db.create_pastie(pastie)
    return jsonify({'pastie': make_public_pastie(the_pastie)}), 201


@api_app.route('/api/pastie/<int:pastie_id>', methods=['PUT'])
@http_auth.login_required
def update_pastie(pastie_id):
    """Update a specific pastie by ID. Returns an HTTP 404 error if the
    requested pastie does not exist. Otherwise returns the updated pastie."""
    pastie = get_pastie_by_id(pastie_id)
    if pastie is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'content' not in request.json:
        abort(400)
    my_pastie = db.update_pastie(pastie_id, {
        "content": request.json.get('content', pastie.content)
    })
    return jsonify({'pastie': make_public_pastie(my_pastie)})


@api_app.route('/api/pastie/<int:pastie_id>', methods=['DELETE'])
@http_auth.login_required
def delete_pastie(pastie_id):
    """Deletes a pastie. Returns an HTTP 404 error if the requested pastie does
    not exist."""
    if not db.pastie_exists(pastie_id):
        abort(404)
    db.delete_pastie(pastie_id)
    return jsonify({'deleted': True})


@api_app.route('/')
def index():
    """Returns some basic information about the pastie server."""
    return f"tammypaste API server v{API_SERVER_VERSION} on port {LISTEN_PORT}"


if __name__ == '__main__':
    app_users = read_userdb()     # pylint disable=invalid-name
    api_app.run(port=LISTEN_PORT, debug=True)
