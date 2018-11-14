"""
DRS De-Registration documents update schema package.
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
from app.api.v1.models.documents import Documents
from marshmallow import Schema, fields, validates, ValidationError, pre_load, pre_dump
from app.api.v1.helpers.validators import *
from app.api.v1.models.deregdetails import DeRegDetails
from app.api.v1.helpers.error_handlers import ALLOWED_FORMATS
from app import app, GLOBAL_CONF


class DeRegDocumentsUpdateSchema(Schema):
    """Schema for De-Registration documents update route."""

    id = fields.Int()
    filename = fields.Str()
    document_id = fields.Int()
    label = fields.Str()
    required = fields.Boolean()
    link = fields.Str()
    dereg_details = fields.Int(required=True, error_messages={'required': 'dereg_details is required'})
    user_id = fields.Str(required=True, error_messages={'required': 'User Id is required'})

    @pre_dump()
    def get_document_label(self, data):
        """Return label of a document."""
        dereg_details = DeRegDetails.get_by_id(data.dereg_id)
        upload_dir_path = GLOBAL_CONF['upload_directory']
        document = Documents.get_document_by_id(data.document_id)
        data.label = document.label
        data.required = Documents.required
        data.link = '{server_dir}/{local_dir}/{file_name}'.format(
                                server_dir=upload_dir_path,
                                local_dir=dereg_details.tracking_id,
                                file_name=data.filename
                            )

    @pre_load()
    def check_reg_id(self, data):
        """Validates request id."""
        dereg_details_id = data['dereg_details']
        dereg_details = DeRegDetails.get_by_id(dereg_details_id)
        if not dereg_details:
            raise ValidationError('The request id provided is invalid', field_names=['dereg_details_id'])
        elif 'user_id' in data and data['user_id'] != dereg_details.user_id:
            raise ValidationError('Permission denied for this request', field_names=['user_id'])

    @pre_load()
    def validate_format(self, data):
        """Validates files format."""
        for filename in data['files'].keys():
            filename = data['files'][filename]
            doc_format = filename.rsplit('.', 1)[1]
            if doc_format not in ALLOWED_FORMATS:
                raise ValidationError('File format {0} is not allowed'.format(doc_format),
                                      field_names=['document_format'])

    @pre_load()
    def validate_file_name(self, data):
        """Validates file names."""
        filenames = []
        for filename in data['files'].keys():
            if data['files'].get(filename) not in filenames:
                filenames.append(data['files'].get(filename))
            else:
                raise ValidationError('File names should be unique',
                                      field_names=['filename'])
