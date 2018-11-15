"""
DRS Technologies Model package.
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
from app import db
from functools import lru_cache


class Technologies(db.Model):
    """Database model for technologies table."""
    __tablename__ = 'technologies'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10), nullable=False)

    @staticmethod
    @lru_cache(maxsize=32)
    def get_technology_id(technology_type):
        """Return a technology id."""
        technology = Technologies.query.filter_by(description=technology_type).first()
        if technology:
            return technology.id
        return technology

    @staticmethod
    @lru_cache(maxsize=32)
    def get_technologies():
        """Return all the supported technologies."""
        return Technologies.query.all()

    @staticmethod
    @lru_cache(maxsize=32)
    def get_technologies_names():
        """Return name of all supported technologies."""
        technologies = Technologies.query.all()
        if technologies:
            return list(map(lambda x: x.description, technologies))
        return []

    @staticmethod
    @lru_cache(maxsize=32)
    def get_technology_by_id(technology_id):
        """Return technology by id."""
        technology = Technologies.query.filter_by(id=technology_id).first()
        if technology:
            return technology.description
        return technology
