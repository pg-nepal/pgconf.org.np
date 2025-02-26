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
    type           = sa.Column(p_attendees_type, server_default=e_attendees_type.participant.name)

    name           = sa.Column(sa.String(50), nullable=False)
    email          = sa.Column(sa.String(256), unique=True, nullable=False)
    phone          = sa.Column(sa.String(10))
    idProofBlob    = sa.Column(sa.LargeBinary, comment='id-card for discount')

    country        = sa.Column(sa.String(30), nullable=False)
    bio            = sa.Column(sa.Text(), comment='basic intro')
    affiliation    = sa.Column(sa.String(256), comment='affiliation & position')
    photoBlob      = sa.Column(sa.LargeBinary)

    category       = sa.Column(sa.String(100), nullable=False, comment='participant category for discount')
    status         = sa.Column(p_attendees_status, server_default='pending')


tickets_type = {
    'main' : 'Main Conference',
    'pre'  : 'Pre Conference Traning',
}
e_tickets_type = enum.StrEnum('tickets_type', tickets_type)
p_tickets_type = sa.Enum(
    e_tickets_type,
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

    attendee_pk    = sa.Column(sa.Integer, sa.ForeignKey(Attendee.pk, ondelete='CASCADE'))

    type           = sa.Column(p_tickets_type, server_default=e_tickets_type.main.name)
    fee            = sa.Column(sa.Numeric(10, 2))

    paidAmount     = sa.Column(sa.Numeric(10, 2), server_default='0')
    receiptBlob    = sa.Column(sa.LargeBinary)
    paymentRef     = sa.Column(sa.Integer)  # self reference; workout needed for case of the multiple self reference

    paymentStatus  = sa.Column(sa.String(10), server_default='unpaid')
    paymentNote    = sa.Column(sa.Text)
    ticketNote     = sa.Column(sa.Text)
