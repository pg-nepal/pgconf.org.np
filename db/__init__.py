# flake8: noqa:F401

import datetime as dt
import os

import sqlalchemy as sa
import sqlalchemy.orm

url = sa.URL.create(
    'postgresql+psycopg',
    username=os.getenv('PG_USER'),
    password=os.getenv('PG_PASSWORD'),
    port=os.getenv('PG_PORT'),
    host=os.getenv('PG_HOST', 'localhost'),
    database=os.getenv('PG_DB', 'pug'),
)

isDebug = bool(os.getenv('DEBUG'))  # direct access
engine = sa.create_engine(
    url=url,
    future=True,
    echo=isDebug,  # default:False
)

SessionMaker = sa.orm.sessionmaker(bind=engine)

meta = sa.MetaData()


class Base(sqlalchemy.orm.DeclarativeBase):
    metadata = meta

    createdOn = sa.Column(sa.DateTime(timezone=True), nullable=False)
    createdBy = sa.Column(sa.String(256))
    updatedOn = sa.Column(sa.DateTime(timezone=True), nullable=False)
    updatedBy = sa.Column(sa.String(32))
