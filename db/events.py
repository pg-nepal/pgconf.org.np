import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

import db


class Register(db.Base):
    __tablename__ = 'registers'
    __table_args__= {
        'schema'  : 'conf25',
        'comment' : 'conference registrations'
    }

    pk            = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name          = sa.Column(sa.String(50), nullable=False)
    email         = sa.Column(sa.String(256), nullable=False)
    registration_id = sa.Column(sa.String(), nullable=False)
    phone         = sa.Column(sa.String(10), nullable=False)
    category      = sa.Column(sa.String(100), nullable=False)
    id_url        = sa.Column(sa.String(256), nullable=True)
    country       = sa.Column(sa.String(100), nullable=False)
    citizen_url   = sa.Column(sa.String(256), nullable=True)
    fee           = sa.Column(sa.Integer, nullable=False)
    status        = sa.Column(
                  ENUM('pending', 'confirmed', 'paid', name='registration_status'),
                  nullable=False,
                  server_default='pending'
    )
    ticket        = sa.Column(sa.String(500), nullable=True)
    createdOn     = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())  # noqa:E501
