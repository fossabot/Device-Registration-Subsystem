"""
DRS Common schema package.
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
from enum import Enum
from marshmallow import Schema, fields


class FileArgs(Schema):
    """Args schema for file downloading route."""

    path = fields.String(required=True, missing='')

    @property
    def fields_dict(self):
        """Convert declared fields to dictionary."""
        return self._declared_fields


class Common(Schema):
    """Response schema for supported technologies, devices & statuses."""

    id = fields.Integer(required=True, description='ID of the type')
    description = fields.String(required=True, description='Description of the type')


class Document(Schema):
    """Response Schema for supported document types."""

    id = fields.Integer(required=True, description='ID of the document')
    label = fields.String(required=True, description='Label of the document')
    type = fields.Integer(required=True, description='Type of the document')
    required = fields.Boolean(required=True, description='Weather the document is required or not')


class Documents(Schema):
    """Response schema for supported documents."""

    registration = fields.List(fields.Nested(Document, required=True),
                               required=False,
                               description='List of supported documents for registration')
    de_registration = fields.List(fields.Nested(Document, required=True),
                                  required=False,
                                  description='List of supported documents for de-registration')


class ServerConfigs(Schema):
    """Response schema for server-config route."""

    technologies = fields.List(fields.Nested(Common, required=True),
                               required=False,
                               description='List of the supported technologies')
    documents = fields.Nested(Documents, required=False, description='Supported document types')
    status_types = fields.List(fields.Nested(Common, required=True),
                               required=False,
                               description='List of the supported status types')
    device_types = fields.List(fields.Nested(Common, required=True),
                               required=False,
                               description='List of the supported device types')


class RequestStatusTypes(Enum):
    """Schema for status types of a request when in the review process."""

    approved = 6
    rejected = 7
    closed = 8
