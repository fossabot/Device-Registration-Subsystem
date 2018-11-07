"""
module for device-quota api tests

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

# pylint: disable=redefined-outer-name
# api urls
DEVICE_QUOTA_API = 'api/v1/review/device-quota'


def test_with_invalid_params(flask_app, db):  # pylint: disable=unused-argument
    """Verify that the device-quota api responds properly when given wrong params."""
    # str instead of int in request_id
    request_id = 'abc'
    rv = flask_app.get('{0}?request_id={1}'.format(DEVICE_QUOTA_API, request_id))
    assert rv.status_code == 422
    data = json.loads(rv.data.decode('utf-8'))
    assert data.get('request_id') == ["Bad 'request_id':'abc' argument format. Accepts only integer"]

    # test with no param
    rv = flask_app.get(DEVICE_QUOTA_API)
    assert rv.status_code == 422
    data = json.loads(rv.data.decode('utf-8'))
    assert data.get('error') == ['parameter request_id is required']


def test_request_not_exist(flask_app, db):  # pylint: disable=unused-argument
    """Verify that device-quota api responds properly when an invalid request_id is given,
    which does not exists in the system.
    """
    request_id = 123131363612863612682816
    rv = flask_app.get('{0}?request_id={1}'.format(DEVICE_QUOTA_API, request_id))
    assert rv.status_code == 204


def test_post_method_not_allowed(flask_app):
    """Verify that POST method is not allowed on device-quota api."""
    rv = flask_app.post(DEVICE_QUOTA_API)
    assert rv.status_code == 405
    data = json.loads(rv.data.decode('utf-8'))
    assert data.get('message') == 'method not allowed'


def test_delete_method_not_allowed(flask_app):
    """Verify that DELETE method is not allowed on device-quota api."""
    rv = flask_app.delete(DEVICE_QUOTA_API)
    assert rv.status_code == 405
    data = json.loads(rv.data.decode('utf-8'))
    assert data.get('message') == 'method not allowed'


def test_put_method_not_allowed(flask_app):
    """Verify that PUT method is not allowed on device-quota api."""
    rv = flask_app.put(DEVICE_QUOTA_API)
    assert rv.status_code == 405
    data = json.loads(rv.data.decode('utf-8'))
    assert data.get('message') == 'method not allowed'
