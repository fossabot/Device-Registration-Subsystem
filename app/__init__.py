"""
Project Initialization package.
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
import sys

from datetime import datetime
from flask_restful import Api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.config import ConfigParser, ParseException

# import _strptime to avoid weird issues as described at
# http://bugs.python.org/msg221094
datetime.strptime('', '')

app = Flask(__name__)
CORS(app)
api = Api(app)

# read and load DRS base configuration to the app
try:
    config = ConfigParser('etc/config.yml').parse_config()
except ParseException as e:
    app.logger.critical('exception encountered while parsing the config file, see details below')
    app.logger.exception(e)
    sys.exit(1)

CORE_BASE_URL = config['dirbs_core']['base_url']  # core api base url
GLOBAL_CONF = config['global']  # load & export global configs
app.config['DRS_UPLOADS'] = config['global']['upload_directory']  # file upload dir
app.config['DRS_LISTS'] = config['lists']['path']  # lists dir
app.config['CORE_BASE_URL'] = config['global']['core_api_v2']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://%s:%s@%s:%s/%s' % \
                                        (config['database']['user'],
                                         config['database']['password'],
                                         config['database']['host'],
                                         config['database']['port'],
                                         config['database']['database'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = config['database']['pool_size']
app.config['SQLALCHEMY_POOL_RECYCLE'] = config['database']['pool_recycle']
app.config['SQLALCHEMY_MAX_OVERFLOW'] = config['database']['max_overflow']
app.config['SQLALCHEMY_POOL_TIMEOUT'] = config['database']['pool_timeout']
# app.config['MAX_CONTENT_LENGTH'] = 28 * 3 * 1024 * 1024

db = SQLAlchemy(session_options={'autocommit': False})
db.init_app(app)

# we really need wild-card import here for now
from app.api.v1.routes import *  # pylint: disable=wildcard-import


@app.after_request
def no_cache(response):
    """Make sure that API responses are not cached by setting headers."""
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    response.cache_control.max_age = 0
    response.headers['Pragma'] = 'no-cache'
    response.expires = 0
    return response


@app.after_request
def add_security_headers(response):
    """Make sure to add security headers to each API response."""
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    if config['server']['restrict_https']:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


register_docs()
