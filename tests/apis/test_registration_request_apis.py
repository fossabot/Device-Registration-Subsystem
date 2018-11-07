"""
module for common apis test

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
import uuid

from tests._fixtures import *  # pylint: disable=wildcard-import
from tests._helpers import create_registraiton

# pylint: disable=redefined-outer-name

DEVICE_REGISTRATION_REQ_API = 'api/v1/registration'
USER_NAME = 'test-abc'
USER_ID = '17102'
IMEIS = "[['86834403015010']]"
REQUEST_DATA = {

    'device_count': 1,
    'imei_per_device': 1,
    'imeis': IMEIS,
    'm_location': 'local',
    'user_name': USER_NAME,
    'user_id': USER_ID

}


def test_device_registration_post_method(flask_app, db):  # pylint: disable=unused-argument
    """ To verify that registration post
        method is working properly and response is correct"""

    headers = {'Content-Type': 'multipart/form-data'}

    rv = flask_app.post(DEVICE_REGISTRATION_REQ_API, data=REQUEST_DATA, headers=headers)
    assert rv.status_code == 200

    data = json.loads(rv.data.decode('utf-8'))
    assert data['user_name'] == USER_NAME
    assert data['user_id'] == USER_ID
    assert data['tracking_id'] is not None
    assert data['status_label'] == 'New Request'
    assert data['report_status_label'] == 'New Request'
    assert data['processing_status_label'] == 'New Request'
    assert data['imeis'] == [['86834403015010']]


def test_device_registration_get_method(flask_app, db):  # pylint: disable=unused-argument
    """ To verify that registration get
        method is working properly and response is correct"""
    request = create_registraiton(REQUEST_DATA, uuid.uuid4())

    api_url = '{api}/{id}'.format(api=DEVICE_REGISTRATION_REQ_API, id=request.id)
    rv = flask_app.get(api_url)
    assert rv.status_code == 200
    data = json.loads(rv.data.decode('utf-8'))
    assert data is not None
    assert data['id'] == request.id


def test_device_registration_put_method_failure(flask_app, db):  # pylint: disable=unused-argument
    """ To verify that registration put
        method gets failed in case of new request response is correct"""

    request = create_registraiton(REQUEST_DATA, uuid.uuid4())
    headers = {'Content-Type': 'multipart/form-data'}
    modified_data = {'m_location': 'overseas', 'reg_id': request.id, 'user_id': USER_ID}
    rv = flask_app.put(DEVICE_REGISTRATION_REQ_API, data=modified_data, headers=headers)
    assert rv.status_code == 422
