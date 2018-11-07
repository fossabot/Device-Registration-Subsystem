"""
DRS Validators package.
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
from marshmallow import ValidationError
import re


def validate_comment(val):
    """Validate input field comment."""
    match = re.match('[a-zA-Z0-9\s]{1,1000}$', val)
    if match is None:
        raise ValidationError("invalid characters not allowed")


def validate_number(val):
    """Validate number input field."""
    match = re.match('^\+?[^\t](?:[0-9]){9,15}[0-9]$', val)
    if match is None:
        raise ValidationError("invalid format")


def date_validation(val):
    """Validate date input field."""
    match = re.match('^((0?[13578]|10|12)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))(-|\/)((19)([0-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))|(0?[2469]|11)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[0]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1})))$', str(val))
    if match is None:
        raise ValidationError("invalid format")


def validate_imei(val):
    """Validate IMEI input field."""
    if not val.isdigit():
        raise ValidationError("invalid imei")


def validate_msisdn(val):
    """Validate MSISDN input field."""
    match = re.match('^\+?(?:[0-9]?){9,15}[0-9]$', val)
    if match is None:
        raise ValidationError("invalid msisdn")


def validate_input(key, value):
    """Validate different input fields."""
    if len(value) == 0 or len(value) > 1000:
        raise ValidationError('{0} value should be between 1 and 1000'.format(key), field_names=[key])
    if value.startswith(' ') or value.endswith(' '):
        raise ValidationError('{0} cannot start or ends with spaces'.format(key), field_names=[key])
    elif value.startswith('\t') or value.endswith('\t'):
        raise ValidationError('{0} cannot start or ends with tabs'.format(key), field_names=[key])
    elif value.startswith('\n') or value.endswith('\n'):
        raise ValidationError('{0} cannot end with line breaks'.format(key), field_names=[key])
