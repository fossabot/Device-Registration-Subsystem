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
import copy

from tests._helpers import create_de_registration
from tests.apis.test_de_registration_request_apis import REQUEST_DATA as DE_REG_REQ_DATA


DEVICE_DE_REGISTRATION_REPORT_API = 'api/v1/deregistration/report'


def test_report_file_invalid_request(flask_app, db):  # pylint: disable=unused-argument
    """ unittest for de-registration report invalid request."""
    url = "{0}/{1}".format(DEVICE_DE_REGISTRATION_REPORT_API, 'abcd')
    rv = flask_app.get(url)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 422
    assert data['message'][0] == 'Registration Request not found.'


def test_report_file_valid_request(flask_app, db):  # pylint: disable=unused-argument
    """ unittest for de-registration report request not found."""
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request = create_de_registration(request_data, uuid.uuid4())

    url = "{0}/{1}".format(DEVICE_DE_REGISTRATION_REPORT_API, request.id)
    rv = flask_app.get(url)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 422
    assert data['message'][0] == 'Report not found.'
