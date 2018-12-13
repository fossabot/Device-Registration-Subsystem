"""
module for search registration module api test

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

from tests._helpers import create_dummy_request, \
    create_dummy_devices, \
    create_assigned_dummy_request, \
    seed_database, \
    create_views

# api urls
SEARCH_API = 'api/v1/search'
DEVICE_REGISTRATION_REQ_API = 'api/v1/registration'


def test_valid_search_specs(flask_app, db):
    """Validate search specs parameters and respond with valid status code."""

    # Check empty result is return
    headers = {'Content-type': 'application/json'}
    body_data = {
        "start": 1,
        "limit": 10,
        "search_specs":
            {
                "group": "reviewer",
                "request_type": 1,
                "user_id": "90X1A-XXXX"
            },
        "search_args":
            {
                "id": "100000"
            }
    }

    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert data['requests'] == []

    # Return all records
    data = {
        'device_count': 1,
        'imei_per_device': 1,
        'imeis': "[['86834403380296']]",
        'm_location': 'local',
        'user_name': 'Test_User_1',
        'user_id': '717'
    }

    request = create_assigned_dummy_request(data, 'Registration', 'Test-Reviewer', 'reviewer-1')
    assert request

    device_data = {
        'brand': 'Honor',
        'operating_system': 'android',
        'model_name': 'Honor 8X',
        'model_num': '8X',
        'device_type': 'Smartphone',
        'technologies': ['2G', '3G', '4G'],
        'reg_id': request.id
    }

    request = create_dummy_devices(device_data, 'Registration', request)
    assert request

    body_data['search_args'] = {}
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 200
    data = json.loads(rv.data.decode('utf-8'))
    assert data['requests'] != []


def test_invalid_search_specs(flask_app):
    """Validate request if invalid parameters or values are provided and respond with proper status code."""
    headers = {'Content-type': 'application/json'}
    body_data = {
        "start": 1,
        "limit": 10,
        "search_specs":
            {
                "group": "reviewer",
                "request_type": "one",
                "user_id": ""
            },
        "search_args":
            {
            }
    }

    # +ve response with empty result
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert data['message'] == "Request type not found!"

    # no data found
    body_data['search_specs']['group'] = ""
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 404
    assert data['message'] == "No data found"

    # empty input parameters
    body_data['search_specs']['group'] = ""
    body_data['search_specs']['request_type'] = ""
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 404
    assert data['message'] == "No data found"


def test_search_invalid_parameters(flask_app, db):
    """Validate invalid seach specification input parameters and respond with proper status code."""

    #
    data = {
        'device_count': 1,
        'imei_per_device': 2,
        'imeis': "[['86834403380268','86834403380269']]",
        'm_location': 'local',
        'user_name': 'Test_User',
        'user_id': '800'
    }

    request = create_assigned_dummy_request(data, 'Registration', 'Test-Reviewer', 'reviewer-1')
    assert request

    device_data = {
        'brand': 'Xiaomi',
        'operating_system': 'android',
        'model_name': 'Mi 8',
        'model_num': 'Mi 8',
        'device_type': 'Smartphone',
        'technologies': ['2G', '3G', '4G'],
        'reg_id': request.id
    }

    request = create_dummy_devices(device_data, 'Registration', request)
    assert request

    headers = {'Content-type': 'application/json'}

    # Reviewer invalid request parameters
    body_data = {
        "start": 1,
        "limit": 10,
        "search_specs":
            {
                "group": "reviewer",
                "request_type": 1,
                "user_id": ""
            },
        "search_args":
            {
                "tracking_id": "string",
                "created_at": "string",
                "updated_at": "string",
                "device_count": "string",
                "status": "string",
                "brand": "string",
                "model_name": "string",
                "operating_system": "string",
                "device_type": "string",
                "imeis": ["string", "string"]
            }
    }
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 404
    assert data['message'] == "Not Found"

    # Individual user invalid parameters
    body_data['search_specs']['group'] = "individual"
    body_data['search_specs']['user_id'] = '800'
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 404
    assert data['message'] == "Not Found"

    # importer user parameters
    body_data['search_specs']['group'] = "importer"
    body_data['search_specs']['user_id'] = '800'
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    data = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 404
    assert data['message'] == "Not Found"
    assert data['requests'] == []


def test_search_valid_parameters(flask_app, db):
    """Validate/Verifies valid search parameters all valid search inputs and respond with proper status code."""

    data = {
        'device_count': 1,
        'imei_per_device': 2,
        'imeis': "[['86834403380270','86834403380271']]",
        'm_location': 'local',
        'user_name': 'Test_User',
        'user_id': '800'
    }

    request = create_assigned_dummy_request(data, 'Registration', 'Test-Reviewer', 'reviewer-1')
    assert request

    device_data = {
        'brand': 'Xiaomi',
        'operating_system': 'android',
        'model_name': 'Mi 8',
        'model_num': 'Mi 8',
        'device_type': 'Smartphone',
        'technologies': ['2G', '3G'],
        'reg_id': request.id
    }

    request = create_dummy_devices(device_data, 'Registration', request)
    assert request

    headers = {'Content-type': 'application/json'}

    # Reviewer Valid request parameters
    body_data = {
        "start": 1,
        "limit": 10,
        "search_specs":
            {
                "group": "reviewer",
                "request_type": 1,
                "user_id": ""
            },
        "search_args":
            {
                "id": request.id,
                "tracking_id": request.tracking_id,
                "brand": device_data['brand'],
                "created_at": request.created_at.strftime("%Y-%m-%d") + ',' + request.updated_at.strftime("%Y-%m-%d"),
                "updated_at": request.created_at.strftime("%Y-%m-%d") + ',' + request.updated_at.strftime("%Y-%m-%d"),
                "device_count": request.device_count,
                "model_name": device_data['model_name'],
                "operating_system": device_data['operating_system'],
                "device_type": device_data['device_type'],
                "imeis": ['86834403380270', '86834403380271'],
                "technologies": device_data['technologies']
            }
    }

    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert result['requests'] != []
    assert rv.status_code == 200

    body_data['search_args'] = {}
    body_data['search_args']['imeis'] = ['86834403380270']
    body_data['search_args']['device_count'] = request.device_count
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert result['requests'] != []
    assert rv.status_code == 200

    body_data['search_args'] = {}
    body_data['search_specs']['group'] = 'importer'
    body_data['search_specs']['user_id'] = data['user_id']
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert result['requests'] != []
    assert rv.status_code == 200

    body_data['search_args'] = {}
    body_data['search_args']['status'] = "In Review"
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert result['requests'] != []
    assert rv.status_code == 200


def test_technologies(flask_app, db):
    """Validate technologies input search parameter and respond with positive result and status code."""

    data = {
        'device_count': 1,
        'imei_per_device': 2,
        'imeis': "[['86834403380270','86834403380271']]",
        'm_location': 'local',
        'user_name': 'Test_User',
        'user_id': '800'
    }

    request = create_assigned_dummy_request(data, 'Registration', 'Test-Reviewer', 'reviewer-1')
    assert request

    device_data = {
        'brand': 'Xiaomi',
        'operating_system': 'android',
        'model_name': 'Mi 8',
        'model_num': 'Mi 8',
        'device_type': 'Smartphone',
        'technologies': ['2G', '3G'],
        'reg_id': request.id
    }

    request = create_dummy_devices(device_data, 'Registration', request)
    assert request

    headers = {'Content-type': 'application/json'}
    body_data = {
        "start": 1,
        "limit": 10,
        "search_specs":
            {
                "group": "reviewer",
                "request_type": 1,
                "user_id": ""
            },
        "search_args":
            {
            }
    }

    body_data['search_args']['technologies'] = device_data['technologies']
    body_data['search_args']['device_count'] = data['device_count']
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert result['requests'] != []
    assert rv.status_code == 200

    body_data['search_args'] = {}
    body_data['search_args']['technologies'] = "3G"
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert result['requests'] != []
    assert rv.status_code == 200


def test_id(flask_app, db):
    """Verifies valid id input search parameter and respond with positive result and status code."""

    data = {
        'device_count': 1,
        'imei_per_device': 2,
        'imeis': "[['86834403380270','86834403380271']]",
        'm_location': 'local',
        'user_name': 'Test_User',
        'user_id': '800'
    }

    request = create_assigned_dummy_request(data, 'Registration', 'Test-Reviewer', 'reviewer-1')
    assert request

    device_data = {
        'brand': 'Xiaomi',
        'operating_system': 'android',
        'model_name': 'Mi 8',
        'model_num': 'Mi 8',
        'device_type': 'Smartphone',
        'technologies': ['2G', '3G'],
        'reg_id': request.id
    }

    request_device = create_dummy_devices(device_data, 'Registration', request)
    assert request_device

    headers = {'Content-type': 'application/json'}

    body_data = {
        "start": 1, "limit": 10,
        "search_specs":
            {
                "group": "importer",
                "request_type": 1,
                "user_id": "800"
            },
        "search_args":
            {
            }
    }

    body_data['search_args']['id'] = request.id
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert result['requests'] != []
    assert rv.status_code == 200


def test_device_count(flask_app, db):
    """Verifies valid device_count input search parameter
    and respond with positive or empty result and status code."""

    data = {
        'device_count': 1,
        'imei_per_device': 2,
        'imeis': "[['86834403380270','86834403380271']]",
        'm_location': 'local',
        'user_name': 'Test_User',
        'user_id': '800'
    }

    request = create_assigned_dummy_request(data, 'Registration', 'Test-Reviewer', 'reviewer-1')
    assert request

    device_data = {
        'brand': 'Xiaomi',
        'operating_system': 'android',
        'model_name': 'Mi 8',
        'model_num': 'Mi 8',
        'device_type': 'Smartphone',
        'technologies': ['2G', '3G'],
        'reg_id': request.id
    }

    request_device = create_dummy_devices(device_data, 'Registration', request)
    assert request_device

    headers = {'Content-type': 'application/json'}

    body_data = {
        "start": 1, "limit": 10,
        "search_specs":
            {
                "group": "importer",
                "request_type": 1,
                "user_id": "800"
            },
        "search_args":
            {
            }
    }

    body_data['search_args']['device_count'] = data['device_count']
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert result['requests'] != []

    body_data['search_args']['device_count'] = 10000
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert result['requests'] == []



def test_request_status(flask_app, db):
    """Verify/Validate and return all approved and pending request."""

    data = {
        'device_count': 1,
        'imei_per_device': 2,
        'imeis': "[['86834403380270','86834403380271']]",
        'm_location': 'local',
        'user_name': 'Test_User',
        'user_id': '800'
    }

    request = create_dummy_request(data, 'Registration', 'Approved')
    assert request

    device_data = {
        'brand': 'Xiaomi',
        'operating_system': 'android',
        'model_name': 'Mi 8',
        'model_num': 'Mi 8',
        'device_type': 'Smartphone',
        'technologies': ['2G', '3G'],
        'reg_id': request.id
    }

    request_device = create_dummy_devices(device_data, 'Registration', request)
    assert request_device

    headers = {'Content-type': 'application/json'}

    body_data = {
        "start": 1, "limit": 10,
        "search_specs":
            {
                "group": "importer",
                "request_type": 1,
                "user_id": "800"
            },
        "search_args":
            {
            }
    }

    body_data['search_args']['status'] = 'Approved'
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert result['requests'] != []

    # Invalid Result
    body_data['search_args'] = {}
    body_data['search_args']['status'] = 'Pending Review'
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert result['requests'] == []


def test_valid_invalid_imei(flask_app, db):
    """Verify/Validate imei's and return all & empty result."""

    data = {
        'device_count': 1,
        'imei_per_device': 2,
        'imeis': "[['86834403380270','86834403380271']]",
        'm_location': 'local',
        'user_name': 'Test_User',
        'user_id': '800'
    }

    request = create_assigned_dummy_request(data, 'Registration', 'Test-Reviewer', 'reviewer-1')
    assert request

    device_data = {
        'brand': 'Xiaomi',
        'operating_system': 'android',
        'model_name': 'Mi 8',
        'model_num': 'Mi 8',
        'device_type': 'Smartphone',
        'technologies': ['2G', '3G'],
        'reg_id': request.id
    }

    request = create_dummy_devices(device_data, 'Registration', request)
    assert request

    headers = {'Content-type': 'application/json'}

    body_data = {
        "start": 1, "limit": 10,
        "search_specs":
            {
                "group": "importer",
                "request_type": 1,
                "user_id": "800"
            },
        "search_args":
            {
            }
    }

    body_data['search_args']['imeis'] = ['86834403380270', '86834403380271']
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    assert rv.status_code == 200

    body_data['search_args'] = {}
    body_data['search_args']['imeis'] = ['86834403380270']
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert result['requests'] != []

    body_data['search_args'] = {}
    body_data['search_args']['imeis'] = ['8683440338027011']
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert result['requests'] == []


def test_valid_invalid_date(flask_app, db):
    """Search by date and return all result of current user and empty search result"""

    data = {
        'device_count': 1,
        'imei_per_device': 2,
        'imeis': "[['86834403380270','86834403380271']]",
        'm_location': 'local',
        'user_name': 'Test_User',
        'user_id': '800'
    }

    request = create_assigned_dummy_request(data, 'Registration', 'Test-Reviewer', 'reviewer-1')
    assert request

    device_data = {
        'brand': 'Xiaomi',
        'operating_system': 'android',
        'model_name': 'Mi 8',
        'model_num': 'Mi 8',
        'device_type': 'Smartphone',
        'technologies': ['2G', '3G'],
        'reg_id': request.id
    }

    request = create_dummy_devices(device_data, 'Registration', request)
    assert request

    headers = {'Content-type': 'application/json'}

    body_data = {
        "start": 1, "limit": 10,
        "search_specs":
            {
                "group": "importer",
                "request_type": 1,
                "user_id": "800"
            },
        "search_args":
            {
            }
    }

    # Valid Date Check
    body_data['search_args']['created_at'] = \
        request.created_at.strftime("%Y-%m-%d") + ',' + request.created_at.strftime("%Y-%m-%d")
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert result['requests'] != []

    body_data['search_args'] = {}
    body_data['search_args']['created_at'] = request.created_at.strftime(
        "%Y-%m-%d") + ',' + request.created_at.strftime("%Y-%m-%d")
    body_data['search_args']['updated_at'] = request.updated_at.strftime(
        "%Y-%m-%d") + ',' + request.updated_at.strftime("%Y-%m-%d")
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert result['requests'] != []

    # InValid Date Check
    body_data['search_args'] = {}
    body_data['search_args']['created_at'] = '2020-12-11' + ',' + '2018-12-11'
    rv = flask_app.post(SEARCH_API, data=json.dumps(body_data), headers=headers)
    result = json.loads(rv.data.decode('utf-8'))
    assert rv.status_code == 200
    assert result['requests'] == []
