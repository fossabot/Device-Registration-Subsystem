"""
DRS Unit Test helper module.

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
from sqlalchemy import text

from scripts.db.seeders import Seed
from scripts.db.views import Views
from app.api.v1.models.regdetails import RegDetails
from app.api.v1.models.deregdetails import DeRegDetails

def seed_database(db):
    """Helper method to seed data into the database."""
    seeder = Seed(db)
    seeder.seed_technologies()
    seeder.seed_status()
    seeder.seed_device_types()
    seeder.seed_documents()


def create_views(db):
    """Helper method to index database and create views."""
    db_views = Views(db)
    db_views.create_registration_view()
    db_views.create_de_registration_view()


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def get_notification_id(session, request_id):
    """Helper Method to extract a notification's id from notification
    table using raw SQL rather than using the sqlalchmey model.
    """
    res = session.execute(text("""SELECT id
                                        FROM public.notification
                                       WHERE request_id='{0}'""".format(request_id))).fetchone()
    return res.id


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def get_single_notification(session, notification_id):
    """Helper method to extract a single notification from notification table."""
    return session.execute(text("""SELECT *
                                    FROM public.notification
                                   WHERE id='{0}'""".format(notification_id))).fetchone()


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def get_user_notifications(session, user_id):
    """Helper method to extract a user's notifications from table."""
    return session.execute(text("""SELECT *
                                              FROM public.notification
                                             WHERE user_id='{0}'""".format(user_id))).fetchall()


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def exists_notification(session, notification_id):
    """Helper method to check if a notification exists."""
    res = session.execute(text("""SELECT EXISTS(
                                        SELECT 1
                                          FROM public.notification
                                         WHERE id='{0}') AS notf""".format(notification_id))).fetchone()
    return res.notf


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def exists_user_notifications(session, user_id):
    """Helper method to check if notifications for user exists."""
    res = session.execute(text("""SELECT EXISTS(
                                    SELECT 1 FROM public.notification WHERE user_id='{0}') AS user"""
                               .format(user_id))).fetchone()
    return res.user


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def delete_user_notifications(session, user_id):
    """Helper method to delete notifications for user."""
    return session.execute(text("""DELETE FROM public.notification
                                   WHERE user_id='{0}'""".format(user_id)))


# registration request creation
def create_registraiton(data, tracking_id):
    """ Helper method to create a registration request"""
    return RegDetails.create(data, tracking_id)


# de_registration request creation
def create_de_registraiton(data, tracking_id):
    """ Helper method to create a registration request"""
    return DeRegDetails.create(data, tracking_id)

