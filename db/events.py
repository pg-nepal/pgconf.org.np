# flake8: noqa:E501

import enum
import uuid

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql

import db


attendees_stage = (
    'pending',
    'confirmed',
    'paid',
)
e_attendees_role = enum.IntEnum('attendees_stage', attendees_stage)
p_attendees_stage = sa.Enum(
    e_attendees_role,
    schema   = 'conf25',
    metadata = db.meta,
)


class Attendee(db.Base):
    __tablename__  = 'attendees'
    __table_args__ = {
        'schema'  : 'conf25',
        'comment' : 'conference registrations',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    slug           = sa.Column(sa.dialects.postgresql.UUID, index=True, default=uuid.uuid4)

    name           = sa.Column(sa.String(50), nullable=False)
    email          = sa.Column(sa.String(256), nullable=False)
    phone          = sa.Column(sa.String(10))

    category       = sa.Column(sa.String(100), nullable=False)
    identityCard   = sa.Column(sa.String(256))
    country        = sa.Column(sa.String(30))

    fee            = sa.Column(sa.Integer)
    status         = sa.Column(p_attendees_stage, server_default='pending')
    ticket         = sa.Column(sa.String(500))
    receiptPath    = sa.Column(sa.String(256))
