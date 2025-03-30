# flake8: noqa:E501
import enum
import sqlalchemy as sa
import uuid


import db

proposal_status = (
    'submitted',
    'pending',
    'in review',
    'accepted',
    'pending',
    'rejected',
)
e_proposal_status = enum.IntEnum('proposal_status', proposal_status)
p_proposal_status = sa.Enum(
    e_proposal_status,
    schema   = 'conf25',
    metadata = db.meta,
)


class Proposal(db.Base):
    __tablename__  = 'proposals'
    __table_args__ = {
        'schema'  : 'conf25',
        'comment' : 'conference proposals',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    slug           = sa.Column(sa.dialects.postgresql.UUID, index=True, default=uuid.uuid4)
    attendee_pk    = sa.Column(sa.Integer)

    name           = sa.Column(sa.String(256), nullable=False)
    email          = sa.Column(sa.String(256))
    country        = sa.Column(sa.String(256))

    # Session Details
    session        = sa.Column(sa.String(50))
    title          = sa.Column(sa.String(100))
    abstract       = sa.Column(sa.Text())

    status         = sa.Column(p_proposal_status, server_default='pending', comment='Acceptance status for a proposal')


class Review(db.Base):
    __tablename__  = 'reviews'
    __table_args__ = {
        'schema'  : 'conf25',
        'comment' : 'conference proposals reviews',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    proposal_pk    = sa.Column(sa.Integer, sa.ForeignKey(Proposal.pk, ondelete='CASCADE'))
    comment        = sa.Column(sa.Text(), nullable=False)


class Rate(db.Base):
    __tablename__  = 'rates'
    __table_args__ = (
        # https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table-configuration
        # keyword arguments can be specified using last argument as a dictionary
        sa.UniqueConstraint('createdBy', 'proposal_pk', name='uq_one_rating_only'),
        {
            'schema'  : 'conf25',
            'comment' : 'conference proposals rating',
        },
    )

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    proposal_pk    = sa.Column(sa.Integer, sa.ForeignKey(Proposal.pk, ondelete='CASCADE'))
    value          = sa.Column(sa.Integer, comment='Overall score')
    score          = sa.Column(sa.JSON, comment='JSON data of all the ratings for a proposal')
