# flake8: noqa:F401

import os
import sqlalchemy as sa
import sqlalchemy.orm


url = sa.URL.create(
    'postgresql',
    username = os.getenv('PG_USER'),
    password = os.getenv('PG_PASSWORD'),
    port     = os.getenv('PG_PORT'),
    host     = os.getenv('PG_HOST', 'localhost'),
    database = os.getenv('PG_DB', 'pug'),
)

engine = sa.create_engine(
    url    = url,
    future = True,
    echo   = True,
)

SessionMaker = sa.orm.sessionmaker(bind=engine)

meta = sa.MetaData()


class Base(sqlalchemy.orm.DeclarativeBase):
    metadata = meta