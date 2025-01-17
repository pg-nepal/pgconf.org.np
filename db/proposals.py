import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

import db


class Proposals(db.Base):
    __tablename__  = 'proposals'
    __table_args__ = {
        'schema'  : 'conf25',
        'comment' : 'conference proposals',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    session_id     = sa.Column(sa.String(36))
    status         = sa.Column(
                  ENUM('accepted', 'pending', 'rejected', name='proposal_status'),
                  nullable=False,
                  server_default='pending'
    )

    name           = sa.Column(sa.String(256), nullable=False)
    email          = sa.Column(sa.String(256))
    country        = sa.Column(sa.String(256))
    category       = sa.Column(sa.String(256), nullable=False)

    # Session Details
    session        = sa.Column(sa.String(50))
    title          = sa.Column(sa.String(100))
    abstract       = sa.Column(sa.String(800))

    createdOn      = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())  # noqa:E501
    createdBy      = sa.Column(sa.String(25))
    updatedOn      = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())  # noqa:E501
    updatedBy      = sa.Column(sa.String(25))
