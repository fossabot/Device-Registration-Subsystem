"""
health checks module
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
import datetime
import requests

from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException

from app import app, db


def database_check():
    """Method to check the database health."""
    response = {
        'check': 'database',
        'output': 'database is available and working',
        'passed': True,
        'time_stamp': datetime.datetime.now()
    }

    try:
        with db.engine.connect() as connection:
            connection.execute('SELECT 1')
            return response
    except SQLAlchemyError as e:
        response['passed'] = False
        response['output'] = str(e)
        return response


def dirbs_core_check():
    """Method to check if dirbs core is available."""
    response = {
        'check': 'dirbs core',
        'output': 'dirbs core is available',
        'passed': True,
        'time_stamp': datetime.datetime.now()
    }

    try:
        requests.get('{0}/version'.format(app.config['CORE_BASE_URL']))
        return response
    except RequestException as e:
        response['passed'] = False
        response['output'] = str(e)
        return response


def dirbs_dvs_check():
    """Method to check if dirbs dvs is available."""
    response = {
        'check': 'dirbs dvs',
        'output': 'dirbs dvs is available',
        'passed': True,
        'time_stamp': datetime.datetime.now()
    }

    try:
        requests.get(app.config['DVS_BASE_URL'])
        return response
    except RequestException as e:
        response['passed'] = False
        response['output'] = str(e)
        return response
