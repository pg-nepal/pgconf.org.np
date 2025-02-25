# flake8: noqa:E501

import enum
import uuid

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql

import db


attendees_status = (
    'pending',
    'confirmed',
    'paid',
)
e_attendees_status = enum.IntEnum('attendees_stage', attendees_status)
p_attendees_status = sa.Enum(
    e_attendees_status,
    schema   = 'conf25',
    metadata = db.meta,
)


class Attendee(db.Base):
    __tablename__  = 'attendees'
    __table_args__ = {
        'schema'  : 'conf25',
        'comment' : 'conference attendees',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    slug           = sa.Column(sa.dialects.postgresql.UUID, index=True, default=uuid.uuid4)

    name           = sa.Column(sa.String(50), nullable=False)
    email          = sa.Column(sa.String(256), unique=True, nullable=False)
    phone          = sa.Column(sa.String(10))

    country        = sa.Column(sa.String(30), nullable=False)

    forMain        = sa.Column(sa.Boolean, comment='main conference')
    forPre         = sa.Column(sa.Boolean, comment='pre confrence')

    category       = sa.Column(sa.String(100), nullable=False, comment='participant category for discount')
    fee            = sa.Column(sa.Integer)
    ticket         = sa.Column(sa.String(500))
    status         = sa.Column(p_attendees_status, server_default='pending')
    receiptBlob    = sa.Column(sa.LargeBinary, comment='payment receipt')
