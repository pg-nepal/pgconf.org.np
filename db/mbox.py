import enum

import sqlalchemy as sa

import db


mobx_type = (
    'email',
    'im-telegram',
    'sms',
)
e_mbox_type = enum.IntEnum('mbox_type', mobx_type)
p_mbox_type = sa.Enum(
    e_mbox_type,
    schema   = 'conf25',
    metadata = db.meta,
)


class MBox(db.Base):
    """
    `ref`        : used to store the back refrence to other table; e.g: slug of attendees
    `isSent`     : will be used by the message sender; false: not sent; true: queued
    """
    __tablename__  = 'mboxes'
    __table_args__ = {
        'schema'  : 'conf25',
        'comment' : 'conference communication outbox',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    ref            = sa.Column(sa.String(100), default=None)
    type           = sa.Column(p_mbox_type, default='email')

    to             = sa.Column(sa.String(1000), index=True, nullable=False)
    cc             = sa.Column(sa.String(1000), index=True, default=None)
    bcc            = sa.Column(sa.String(1000), index=True, default=None)

    subject        = sa.Column(sa.String(1000), nullable=False)
    body           = sa.Column(sa.Text, nullable=False)
    note           = sa.Column(sa.Text, default=None)

    isSent         = sa.Column(sa.Boolean, default=False)
