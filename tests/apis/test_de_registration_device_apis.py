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

from tests._helpers import create_de_registration, create_dummy_request, create_dummy_devices
from tests.apis.test_de_registration_request_apis import REQUEST_DATA as DE_REG_REQ_DATA

# pylint: disable=redefined-outer-name

DE_REGISTRATION_DEVICE_API = 'api/v1/deregistration/devices'
USER_ID = '17102'
TAC = '12345'
USER_NAME = 'test-abc'
BRAND = 'Apple'
OPERATING_SYSTEM = 'osx'
MODEL_NAME = 'Iphone-X'
MODEL_NUMBER = '702-TEST'
DEVICE_TYPE = 'Tablet'
TECHNOLOGIES = '3G'
COUNT = 1

REQUEST_DATA = {
    'devices': [{
        'tac': TAC,
        'model_name': MODEL_NAME,
        'brand_name': BRAND,
        'model_num': MODEL_NUMBER,
        'technology': TECHNOLOGIES,
        'device_type': DEVICE_TYPE,
        'count': COUNT,
        'operating_system': OPERATING_SYSTEM
    }],
    'dereg_id': 123,
}


def test_device_post_method_de_reg_id_not_found(flask_app, db):  # pylint: disable=unused-argument
    """ To verify that registration device
        method is working properly and response is correct"""

    headers = {'Content-Type': 'multipart/form-data'}
    request_data = copy.deepcopy(REQUEST_DATA)

    rv = flask_app.post(DE_REGISTRATION_DEVICE_API, data=json.dumps(request_data), headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 422
    assert 'message' in data
    assert data['message'][0] == 'De-Registration Request not found.'


def test_de_registration_devices_success(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'Awaiting Documents')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {
        'devices': """[
                    {
                        "tac": "35700102",
                        "model_name": "TA-1034",
                        "brand_name": "NOKIA",
                        "model_num": "TA-1034",
                        "technology": "NONE",
                        "device_type": "Mobile Phone/Feature phone",
                        "count": 2,
                        "operating_system": "N/A"
                    }
                ]""",
        'dereg_id': de_registration.id
    }
    de_registration = create_dummy_devices(device_data, 'De_Registration', de_registration, db,
                                           file_content=['121621090005119'],
                                           file_path='{0}/{1}/{2}'.format(app.config['DRS_UPLOADS'],
                                                                          de_registration.tracking_id,
                                                                          request_data['file']))

    rv = flask_app.get("{0}/{1}".format(DE_REGISTRATION_DEVICE_API, de_registration.id),
                        data=request_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 200
    assert 'model_num' in data[0]
    assert 'count' in data[0]
    assert 'brand_name' in data[0]
    assert 'device_type' in data[0]


def test_de_registration_devices_invalid_status(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'Awaiting Documents')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'devices': """[{"tac":"35700102","model_name":"TA-1034","brand_name":"NOKIA","model_num":"TA-1034","technology":"NONE","device_type":"Mobile Phone/Feature phone","count":2,"operating_system":"N/A"}]""",
                   'dereg_id': de_registration.id
                   }
    rv = flask_app.post(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 422
    assert 'status' in data
    assert data['status'][0] == 'This step can only be performed for New Request'


def test_de_registration_devices_user_id_missing(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'New Request')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'devices': """[{"tac":"35700102","model_name":"TA-1034","brand_name":"NOKIA","model_num":"TA-1034","technology":"NONE","device_type":"Mobile Phone/Feature phone","count":2,"operating_system":"N/A"}]""",
                   'dereg_id': de_registration.id
                   }
    rv = flask_app.post(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 422
    assert 'user_id' in data
    assert data['user_id'][0] == 'User Id is required'


def test_de_registration_devices_creating_invalid_resp(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'New Request')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'devices': """[{"tac":"35700102","model_name":"TA-1034","brand_name":"NOKIA","model_num":"TA-1034","technology":"NONE","device_type":"Mobile Phone/Feature phone","count":2,"operating_system":"N/A"}]""",
                   'dereg_id': de_registration.id,
                   'user_id': USER_ID
                   }
    rv = flask_app.post(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 500
    assert 'message' in data
    assert data['message'][0] == 'Failed to retrieve response, please try later'


def test_de_registration_devices_creating_missing_model_name(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'New Request')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'devices': """[{"tac":"35700102","brand_name":"NOKIA","model_num":"TA-1034","technology":"NONE","device_type":"Mobile Phone/Feature phone","count":2,"operating_system":"N/A"}]""",
                   'dereg_id': de_registration.id,
                   'user_id': USER_ID
                   }
    rv = flask_app.post(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 422
    assert 'devices' in data
    assert data['devices']['0']['model_name'][0] == 'model_name is a required field'


def test_de_registration_devices_missing_devices(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'Awaiting Documents')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'dereg_id': de_registration.id}
    rv = flask_app.post(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 422


def test_device_put_method_de_reg_id_not_found(flask_app, db):  # pylint: disable=unused-argument
    """ To verify that registration device
        method is working properly and response is correct"""

    headers = {'Content-Type': 'multipart/form-data'}
    request_data = copy.deepcopy(REQUEST_DATA)

    rv = flask_app.post(DE_REGISTRATION_DEVICE_API, data=json.dumps(request_data), headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 422
    assert 'message' in data
    assert data['message'][0] == 'De-Registration Request not found.'


def test_de_registration__update_devices_success(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'Awaiting Documents')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {
        'devices': """[
                    {
                        "tac": "35700102",
                        "model_name": "TA-1034",
                        "brand_name": "NOKIA",
                        "model_num": "TA-1034",
                        "technology": "NONE",
                        "device_type": "Mobile Phone/Feature phone",
                        "count": 2,
                        "operating_system": "N/A"
                    }
                ]""",
        'dereg_id': de_registration.id
    }
    de_registration = create_dummy_devices(device_data, 'De_Registration', de_registration, db,
                                           file_content=['121621090005119'],
                                           file_path='{0}/{1}/{2}'.format(app.config['DRS_UPLOADS'],
                                                                          de_registration.tracking_id,
                                                                          request_data['file']))

    rv = flask_app.get("{0}/{1}".format(DE_REGISTRATION_DEVICE_API, de_registration.id),
                        data=request_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 200
    assert 'model_num' in data[0]
    assert 'count' in data[0]
    assert 'brand_name' in data[0]
    assert 'device_type' in data[0]


def test_de_registration_devices_update_invalid_status(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'New Request')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'devices': """[{"tac":"35700102","model_name":"TA-1034","brand_name":"NOKIA","model_num":"TA-1034","technology":"NONE","device_type":"Mobile Phone/Feature phone","count":2,"operating_system":"N/A"}]""",
                   'dereg_id': de_registration.id
                   }
    rv = flask_app.put(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))


def test_de_registration_devices_update_user_id_missing(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'Pending Review')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'devices': """[{"tac":"35700102","model_name":"TA-1034","brand_name":"NOKIA","model_num":"TA-1034","technology":"NONE","device_type":"Mobile Phone/Feature phone","count":2,"operating_system":"N/A"}]""",
                   'dereg_id': de_registration.id
                   }
    rv = flask_app.put(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 422
    assert 'user_id' in data
    assert data['user_id'][0] == 'User Id is required'


def test_de_registration_devices_update_creating_invalid_resp(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'Pending Review')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'devices': """[{"tac":"35700102","model_name":"TA-1034","brand_name":"NOKIA","model_num":"TA-1034","technology":"NONE","device_type":"Mobile Phone/Feature phone","count":2,"operating_system":"N/A"}]""",
                   'dereg_id': de_registration.id,
                   'user_id': USER_ID
                   }
    rv = flask_app.put(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 500
    assert 'message' in data
    assert data['message'][0] == 'Failed to retrieve response, please try later'


def test_de_registration_devices_update_creating_missing_model_name(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'Pending Review')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'devices': """[{"tac":"35700102","brand_name":"NOKIA","model_num":"TA-1034","technology":"NONE","device_type":"Mobile Phone/Feature phone","count":2,"operating_system":"N/A"}]""",
                   'dereg_id': de_registration.id,
                   'user_id': USER_ID
                   }
    rv = flask_app.put(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 422
    assert 'devices' in data
    assert data['devices']['0']['model_name'][0] == 'model_name is a required field'


def test_de_registration_devices_update_missing_devices(flask_app, app, db):  # pylint: disable=unused-argument
    request_data = copy.deepcopy(DE_REG_REQ_DATA)
    request_data['file'] = 'de-reg-test-file.txt'
    de_registration = create_dummy_request(request_data, 'De-Registration', 'Pending Review')
    headers = {'Content-Type': 'multipart/form-data'}

    device_data = {'dereg_id': de_registration.id}
    rv = flask_app.put(DE_REGISTRATION_DEVICE_API, data=device_data, headers=headers)
    data = json.loads(rv.data.decode('utf-8'))

    assert rv.status_code == 422
