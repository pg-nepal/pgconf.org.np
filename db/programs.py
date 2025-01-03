# flake8: noqa:E501

import sqlalchemy as sa

import db


class Proposal(db.Base):
    __tablename__  = 'proposals'
    __table_args__ = {
        'schema'  : 'conf25',
        'comment' : 'conference proposals',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    name           = sa.Column(sa.String(256), nullable=False)
    email          = sa.Column(sa.String(256))
    address        = sa.Column(sa.String(256))
    country        = sa.Column(sa.String(256))
    phone          = sa.Column(sa.String(10))
    category       = sa.Column(sa.String(256), nullable=False)

    # Session Details
    session        = sa.Column(sa.String(50))
    title          = sa.Column(sa.String(100))
    abstract       = sa.Column(sa.Text())
