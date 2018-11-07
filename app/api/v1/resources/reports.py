"""
DRS report resource package.
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
import os

from flask import Response, send_file
from flask_restful import Resource
from marshmallow import ValidationError

from app import app, db
from app.api.v1.helpers.error_handlers import REG_NOT_FOUND_MSG, REPORT_NOT_FOUND_MSG
from app.api.v1.helpers.response import MIME_TYPES, CODES
from app.api.v1.helpers.utilities import Utilities
from app.api.v1.models.deregdetails import DeRegDetails
from app.api.v1.models.regdetails import RegDetails


class RegistrationReportRoutes(Resource):
    """Class for handling Registration Report Routes."""

    @staticmethod
    def get(reg_id):
        """GET method handler, return registration report."""
        if not reg_id.isdigit() or not RegDetails.exists(reg_id):
            return Response(json.dumps(REG_NOT_FOUND_MSG), status=CODES.get("UNPROCESSABLE_ENTITY"),
                            mimetype=MIME_TYPES.get("APPLICATION_JSON"))
        try:
            req = RegDetails.get_by_id(reg_id)
            if not req.report:
                return Response(json.dumps(REPORT_NOT_FOUND_MSG), status=CODES.get("UNPROCESSABLE_ENTITY"),
                                mimetype=MIME_TYPES.get("APPLICATION_JSON"))
            report = os.path.join(Utilities.upload_directoy, req.tracking_id, req.report)
            return send_file(report)
        except Exception as e:
            app.logger.exception(e)

            data = {
                "message": "Error retrieving results. Please check document_type or database connection."
            }

            response = Response(json.dumps(data), status=CODES.get("BAD_REQUEST"),
                                mimetype=MIME_TYPES.get("APPLICATION_JSON"))
            return response
        finally:
            db.session.close()


class DeRegistrationReportRoutes(Resource):
    """Class for handling De-Registration Report routes."""

    @staticmethod
    def get(dereg_id):
        """GET method handler, returns reports."""
        if not dereg_id.isdigit() or not DeRegDetails.exists(dereg_id):
            return Response(json.dumps(REG_NOT_FOUND_MSG), status=CODES.get("UNPROCESSABLE_ENTITY"),
                            mimetype=MIME_TYPES.get("APPLICATION_JSON"))
        try:
            req = DeRegDetails.get_by_id(dereg_id)
            if not req.report:
                return Response(json.dumps(REPORT_NOT_FOUND_MSG), status=CODES.get("UNPROCESSABLE_ENTITY"),
                                mimetype=MIME_TYPES.get("APPLICATION_JSON"))
            report = os.path.join(Utilities.upload_directoy, req.tracking_id, req.report)
            return send_file(report)
        except Exception as e:
            app.logger.exception(e)

            data = {
                "message": "Error retrieving results. Please check document_type or database connection."
            }

            response = Response(json.dumps(data), status=CODES.get("BAD_REQUEST"),
                                mimetype=MIME_TYPES.get("APPLICATION_JSON"))
            return response
        finally:
            db.session.close()
