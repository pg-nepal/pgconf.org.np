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

attendees_type = (
    'organizer',
    'volunteers',
    'participant',
    'speaker',
    'guest',
)
e_attendees_type = enum.IntEnum('attendees_type', attendees_type)
p_attendees_type = sa.Enum(
    e_attendees_type,
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
    bio            = sa.Column(sa.Text(), comment='basic intro')
    affiliation    = sa.Column(sa.String(256), comment='affiliation & position')
    photoBlob      = sa.Column(sa.LargeBinary)

    forMain        = sa.Column(sa.Boolean, comment='main conference')
    forPre         = sa.Column(sa.Boolean, comment='pre confrence')

    category       = sa.Column(sa.String(100), nullable=False, comment='participant category for discount')
    fee            = sa.Column(sa.Integer)
    ticket         = sa.Column(sa.String(500))
    status         = sa.Column(p_attendees_status, server_default='pending')
    receiptBlob    = sa.Column(sa.LargeBinary, comment='payment receipt')


ticket_types = (
    'Main Conference',
    'Pre-Conference Training',
)
e_ticket_type = enum.IntEnum('ticket_types', ticket_types)
p_ticket_type = sa.Enum(
    e_ticket_type,
    schema   = 'conf25',
    metadata = db.meta,
)


class Ticket(db.Base):
    __tablename__  = 'tickets'
    __table_args__ = {
        'schema'  : 'conf25',
        'comment' : 'conference registrations tickets',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    attendees_pk   = sa.Column(sa.Integer, nullable=False)

    ticketType     = sa.Column(p_ticket_type, server_default='Main Conference')
    fee            = sa.Column(sa.Numeric(10,2))

    paidAmt            = sa.Column(sa.Numeric(10,2))
    paymentReceiptFile = sa.Column(sa.LargeBinary)
    paymentLinkedTo    = sa.Column(sa.Integer) # self reference; workout needed for case of the multiple self reference

    paymentStatus  = sa.Column(sa.String(10), server_default='unpaid')
    paymentNote    = sa.Column(sa.Text)

    ticketNumber   = sa.Column(sa.String(256))
    ticketNote     = sa.Column(sa.Text)
