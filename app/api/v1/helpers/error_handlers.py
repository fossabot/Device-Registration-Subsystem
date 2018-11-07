"""
DRS Error Handler package.
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

from marshmallow import fields, validate
from flask import Response
from app import app
from app.api.v1.helpers.response import CODES, MESSAGES, MIME_TYPES


# custom base 404 error handler
# noinspection PyUnusedLocal
@app.errorhandler(CODES.get('NOT_FOUND'))
def not_found_handler(error):
    """Custom error handler for 404."""
    data = {
        'message': MESSAGES.get('RESOURCE_NOT_FOUND')
    }

    response = Response(json.dumps(data), status=CODES.get('NOT_FOUND'),
                        mimetype=MIME_TYPES.get('APPLICATION_JSON'))
    return response


@app.errorhandler(422)
def validation_errors(error):
    """Transform marshmallow validation errors to custom responses to maintain backward-compatibility."""
    field_name = error.exc.field_names[0]
    field_value = error.exc.data[field_name]
    field_type = error.exc.fields[0]
    if isinstance(field_type, fields.List):
        field_type = error.exc.fields[0].container
        field_value = error.exc.data[field_name][next(iter(error.exc.messages[field_name]))]

    error_response = {
        field_name: [
            get_error_desc(field_type, field_name, field_value)
        ]
    }
    return Response(json.dumps(error_response), status=422,
                    mimetype='application/json')


def get_error_desc(field, name, value):
    """Helper function to construct error description."""
    error_desc = 'Bad \'{0}\':\'{1}\' argument format.'.format(name, value)
    if isinstance(field, fields.Integer):
        try:
            int(value)
            msg_allow_zero = 'or equal to ' if field.validate.min < 1 else ''
            error_desc = 'Param \'{0}\':\'{1}\' must be greater than {2}0' \
                .format(name, value, msg_allow_zero)
        except ValueError:
            error_desc = 'Bad \'{0}\':\'{1}\' argument format. Accepts only integer'.format(name, value)
    if isinstance(field, fields.Boolean):
        allowed_values = ['0', '1', 'true', 'false']
        error_desc = 'Bad \'{0}\':\'{1}\' argument format. Accepts only one of {2}' \
            .format(name, value, allowed_values)
    if isinstance(field, fields.String) and isinstance(field.validate, validate.OneOf):
        error_desc = 'Bad \'{0}\':\'{1}\' argument format. Accepts only one of {2}' \
            .format(name, value, field.validate.choices)
    if isinstance(field, fields.DateTime):
        dateformat = 'YYYYMMDD' if field.dateformat == '%Y%m%d' else field.dateformat
        error_desc = 'Bad \'{0}\':\'{1}\' argument format. Date must be in \'{2}\' format.' \
            .format(name, value, dateformat)
    return error_desc


# flask-restful custom errors
CustomErrors = {
    'MethodNotAllowed': {
        'message': 'method not allowed',
        'status': 405
    }
}

REG_NOT_FOUND_MSG = {'message': ['Registration Request not found.']}
DEREG_NOT_FOUND_MSG = {'message': ['De-Registration Request not found.']}
REPORT_NOT_FOUND_MSG = {'message': ['Report not found.']}
DOC_NOT_FOUND_MSG = {'message': ['Document not found.']}

ALLOWED_FORMATS = ['pdf', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'svg']

