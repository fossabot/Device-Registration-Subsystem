"""
module for review submit-review api tests

Copyright (c) 2018 Qualcomm Technologies, Inc.

 All rights reserved.



 Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the
 limitations in the disclaimer below) provided that the following conditions are met:


 * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
 disclaimer.

 * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
 disclaimer in the documentation and/or other materials provided with the distribution.

 * Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or promote
 products derived from this software without specific prior written permission.

 NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY
 THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
 TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
"""
import json

from tests._fixtures import *  # pylint: disable=wildcard-import

# pylint: disable=redefined-outer-name,unused-argument
# api urls
SUBMIT_REVIEW_API = 'api/v1/review/submit-review'


def test_invalid_input_params(flask_app):
    """Verify that api responds properly when invalid input supplied."""
    # str instead of int in request_id field
    headers = {'Content-Type': 'application/json'}
    body_data = {
        'request_id': 'abcd',
        'request_type': 'registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 422
    data = json.loads(rv.data.decode('utf-8'))
    assert data['request_id'] == ["Bad 'request_id':'abcd' argument format. Accepts only integer"]

    # int instead of str in request_type
    body_data['request_id'] = 1
    body_data['request_type'] = 2
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 422
    data = json.loads(rv.data.decode('utf-8'))
    assert data['request_type'] == ["Bad 'request_type':'2' argument format. Accepts only one of ["
                                    "'registration_request', 'de_registration_request']"]

    # other str than registration_request/de_registration_request in request_type
    body_data['request_type'] = 'abcd'
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 422
    data = json.loads(rv.data.decode('utf-8'))
    assert data['request_type'] == ["Bad 'request_type':'abcd' argument format. Accepts only one of ["
                                    "'registration_request', 'de_registration_request']"]

    # int instead of str in reviewer_id
    body_data['request_type'] = 'registration_request'
    body_data['reviewer_id'] = 1
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 422
    data = json.loads(rv.data.decode('utf-8'))
    assert data['reviewer_id'] == ["Bad 'reviewer_id':'1' argument format."]


def test_null_input_params(flask_app):
    """Verify that the api returns proper error response when no params are given."""
    headers = {'Content-Type': 'application/json'}

    # no request id argument
    body_data = {
        'request_type': 'registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 422
    data = json.loads(rv.data.decode('utf-8'))
    assert data['error'] == ["request_id is required"]

    # no request_type argument
    body_data['request_id'] = 1
    del body_data['request_type']
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 422
    data = json.loads(rv.data.decode('utf-8'))
    assert data['error'] == ["request_type is required"]

    # no reviewer_id argument
    body_data['request_type'] = 'registration_request'
    del body_data['reviewer_id']
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 422
    data = json.loads(rv.data.decode('utf-8'))
    assert data['error'] == ["reviewer_id is required"]


def test_request_not_exists(flask_app, db):
    """Verify that api responds for request which does not exists in system."""
    # registration_request test
    headers = {'Content-Type': 'application/json'}
    body_data = {
        'request_id': 37284234802304802384,
        'request_type': 'registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 204

    # de registration request
    body_data['request_type'] = 'de_registration_request'
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 204


def test_post_method_not_allowed(flask_app):
    """Verify that POST method is not allowed on api."""
    rv = flask_app.post(SUBMIT_REVIEW_API)
    assert rv.status_code == 405
    data = json.loads(rv.data.decode('utf-8'))
    assert data.get('message') == 'method not allowed'


def test_delete_method_not_allowed(flask_app):
    """Verify that DELETE method is not allowed on api."""
    rv = flask_app.delete(SUBMIT_REVIEW_API)
    assert rv.status_code == 405
    data = json.loads(rv.data.decode('utf-8'))
    assert data.get('message') == 'method not allowed'


def test_get_method_not_allowed(flask_app):
    """Verify that PUT method is not allowed on api."""
    rv = flask_app.get(SUBMIT_REVIEW_API)
    assert rv.status_code == 405
    data = json.loads(rv.data.decode('utf-8'))
    assert data.get('message') == 'method not allowed'
