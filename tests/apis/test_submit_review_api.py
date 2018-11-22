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

from tests._helpers import create_dummy_request, create_assigned_dummy_request, create_dummy_devices
from app.api.v1.models.approvedimeis import ApprovedImeis
from app.api.v1.models.regcomments import RegComments
from app.api.v1.models.deregcomments import DeRegComments
from app.api.v1.models.notification import Notification

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


def test_request_not_exists(flask_app, db):  # pylint: disable=unused-argument
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


def test_submitted_registration_requests(flask_app, db):
    """Verify that the api reponds properly when request is already
    approved, ejected or closed.
    """
    # approved request
    headers = {'Content-Type': 'application/json'}
    data = {
        'device_count': 1,
        'imei_per_device': 1,
        'imeis': "[['86834403015010']]",
        'm_location': 'local',
        'user_name': 'assign rev user 1',
        'user_id': 'assign-rev-user-1'
    }

    # registration request test, creating dummy request
    request = create_dummy_request(data, 'Registration', 'Approved')
    assert request
    assert request.status == 6
    request_id = request.id
    body_data = {
        'request_id': request_id,
        'request_type': 'registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 400
    assert json.loads(rv.data.decode('utf-8'))['error'] == ['Request cannot be entertained, '
                                                            'request is already approved']

    # closed request
    data = {
        'device_count': 1,
        'imei_per_device': 1,
        'imeis': "[['86834403015010']]",
        'm_location': 'local',
        'user_name': 'assign rev user 1',
        'user_id': 'assign-rev-user-1'
    }

    # registration request test, creating dummy request
    request = create_dummy_request(data, 'Registration', 'Closed')
    assert request
    assert request.status == 8
    request_id = request.id
    body_data = {
        'request_id': request_id,
        'request_type': 'registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 400
    assert json.loads(rv.data.decode('utf-8'))['error'] == ['Request cannot be entertained, '
                                                            'request is already closed']

    # rejected request
    data = {
        'device_count': 1,
        'imei_per_device': 1,
        'imeis': "[['86834403015010']]",
        'm_location': 'local',
        'user_name': 'assign rev user 1',
        'user_id': 'assign-rev-user-1'
    }

    # registration request test, creating dummy request
    request = create_dummy_request(data, 'Registration', 'Rejected')
    assert request
    assert request.status == 7
    request_id = request.id
    body_data = {
        'request_id': request_id,
        'request_type': 'registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 400
    assert json.loads(rv.data.decode('utf-8'))['error'] == ['Request cannot be entertained, '
                                                            'request is already rejected']


def test_submitted_de_registration_requests(flask_app, db):
    """Verify that the api reponds properly when request is already
    approved, ejected or closed."""
    # approved request
    headers = {'Content-Type': 'application/json'}
    data = {
        'file': 'de-reg-test-file',
        'device_count': 1,
        'user_id': 'assign-rev-user-1',
        'user_name': 'assign rev user 1',
        'reason': 'because we have to run tests successfully'
    }
    request = create_dummy_request(data, 'De-Registration', 'Approved')
    assert request
    assert request.status == 6
    request_id = request.id
    body_data = {
        'request_id': request_id,
        'request_type': 'de_registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 400
    assert json.loads(rv.data.decode('utf-8'))['error'] == ['Request cannot be entertained, '
                                                            'request is already approved']

    # closed request
    data = {
        'file': 'de-reg-test-file',
        'device_count': 1,
        'user_id': 'assign-rev-user-1',
        'user_name': 'assign rev user 1',
        'reason': 'because we have to run tests successfully'
    }
    request = create_dummy_request(data, 'De-Registration', 'Closed')
    assert request
    assert request.status == 8
    request_id = request.id
    body_data = {
        'request_id': request_id,
        'request_type': 'de_registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 400
    assert json.loads(rv.data.decode('utf-8'))['error'] == ['Request cannot be entertained, '
                                                            'request is already closed']

    # rejected request
    data = {
        'file': 'de-reg-test-file',
        'device_count': 1,
        'user_id': 'assign-rev-user-1',
        'user_name': 'assign rev user 1',
        'reason': 'because we have to run tests successfully'
    }
    request = create_dummy_request(data, 'De-Registration', 'Rejected')
    assert request
    assert request.status == 7
    request_id = request.id
    body_data = {
        'request_id': request_id,
        'request_type': 'de_registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 400
    assert json.loads(rv.data.decode('utf-8'))['error'] == ['Request cannot be entertained, '
                                                            'request is already rejected']


def test_invalid_reviewer_id(flask_app, db):
    """Verify that only assigned reviewer can submit the review and api responds properly"""
    # registration request
    headers = {'Content-Type': 'application/json'}
    data = {
        'device_count': 1,
        'imei_per_device': 1,
        'imeis': "[['86834403015010']]",
        'm_location': 'local',
        'user_name': 'assign rev user 1',
        'user_id': 'assign-rev-user-1'
    }
    request = create_assigned_dummy_request(data, 'Registration', 'rev230987', 'rev 230987')
    assert request
    assert request.reviewer_id == 'rev230987'
    request_id = request.id
    body_data = {
        'request_id': request_id,
        'request_type': 'registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 400
    assert json.loads(rv.data.decode('utf-8'))['error'] == ['invalid reviewer rev1']

    # de registration request
    data = {
        'file': 'de-reg-test-file',
        'device_count': 1,
        'user_id': 'assign-rev-user-1',
        'user_name': 'assign rev user 1',
        'reason': 'because we have to run tests successfully'
    }
    request = create_assigned_dummy_request(data, 'De-Registration', 'rev342567', 'rev 23')
    assert request
    assert request.reviewer_id == 'rev342567'
    request_id = request.id
    body_data = {
        'request_id': request_id,
        'request_type': 'de_registration_request',
        'reviewer_id': 'rev1'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 400
    assert json.loads(rv.data.decode('utf-8'))['error'] == ['invalid reviewer rev1']


def test_registration_request_rejected_section(flask_app, db):
    """Verify that the registration request gets rejected when anyone of the section
    is marked as rejected, imeis are removed from approvedimeis and notification is
    being generated.
    """
    # only one section is reviewed and rejected
    headers = {'Content-Type': 'application/json'}
    data = {
        'device_count': 1,
        'imei_per_device': 1,
        'imeis': "[['23010403010533']]",
        'm_location': 'local',
        'user_name': '23423423rev user 1',
        'user_id': 'assign-rev23442342-user-1'
    }
    request = create_assigned_dummy_request(data, 'Registration', 'rev230987', 'rev 230987')
    assert request
    request_id = request.id
    device_data = {
        'brand': 'samsung',
        'operating_system': 'android',
        'model_name': 's9',
        'model_num': '30jjd',
        'device_type': 'Smartphone',
        'technologies': '2G,3G,4G',
        'reg_id': request.id
    }
    request = create_dummy_devices(device_data, 'Registration', request)
    assert request
    # add one section with rejected status
    RegComments.add('device_quota', 'test comment on section', 'rev230987', 'rev 230987', 7, request_id)
    body_data = {
        'request_id': request_id,
        'request_type': 'registration_request',
        'reviewer_id': 'rev230987'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 201
    response = json.loads(rv.data.decode('utf-8'))
    assert response['status'] == 7
    assert response['request_id'] == request_id
    assert response['message'] == 'case {0} updated successfully'.format(request_id)
    assert response['request_type'] == 'registration_request'
    imei = ApprovedImeis.get_imei('23010403010533')
    assert imei.status == 'removed'
    assert imei.delta_status == 'remove'
    assert Notification.exist_users('assign-rev23442342-user-1')


def test_de_registration_request_rejected_section(flask_app, db, app):
    """Verify that the de_registration request gets rejected when anyone of the section
        is marked as rejected, imeis are removed from approvedimeis and notification is
        being generated.
        """
    # de registration request
    headers = {'Content-Type': 'application/json'}
    de_registration_data = {
        'file': 'de-reg-test-file.txt',
        'device_count': 1,
        'user_id': 'dereg-section-submit-assign-rev-user-1',
        'user_name': 'submit assign rev user 1',
        'reason': 'because we have to run tests successfully'
    }
    request = create_assigned_dummy_request(de_registration_data, 'De_Registration', 'dereg-rejected-section-rev', 'de reg rev')
    device_data = {
        'devices': """[
               {
                   "tac": "95762201",
                   "model_name": "TA-1034",
                   "brand_name": "NOKIA",
                   "model_num": "TA-1034",
                   "technology": "NONE",
                   "device_type": "Mobile Phone/Feature phone",
                   "count": 2,
                   "operating_system": "N/A"
               }
           ]""",
        'dereg_id': request.id
    }
    request = create_dummy_devices(device_data, 'De_Registration', request, db, file_content=['957622010005119'],
                                   file_path='{0}/{1}/{2}'.format(app.config['DRS_UPLOADS'], request.tracking_id,
                                                                  de_registration_data.get('file')))
    assert request
    request_id = request.id
    DeRegComments.add('device_description', 'test comment on section', 'dereg-rejected-section-rev', 'rev 230987', 7, request_id)
    body_data = {
        'request_id': request_id,
        'request_type': 'de_registration_request',
        'reviewer_id': 'dereg-rejected-section-rev'
    }
    rv = flask_app.put(SUBMIT_REVIEW_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 201
    response = json.loads(rv.data.decode('utf-8'))
    assert response['status'] == 7
    assert response['request_id'] == request_id
    assert response['message'] == 'case {0} updated successfully'.format(request_id)
    assert response['request_type'] == 'de_registration_request'
    assert Notification.exist_users('dereg-section-submit-assign-rev-user-1')


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
