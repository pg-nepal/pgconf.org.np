#!venv/bin/python

import datetime as dt

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql

import db
import db.mbox
import db.conf
import db.programs


def main(schemas):
    with db.engine.begin() as conn:
        for schema in schemas:
            conn.execute(sa.text('CREATE SCHEMA IF NOT EXISTS {}'.format(schema))) # noqa: E501

    db.meta.create_all(bind=db.engine, checkfirst=True)

    with db.engine.begin() as conn:
        conn.execute(sa.dialects.postgresql.insert(
            db.conf.Event,
        ).values([
            {
                'pk'      : 1,
                'name'    : 'Pre Conference Traning',
                'eventOn' : dt.datetime(2025, 5, 3),
                'eventTo' : dt.datetime(2025, 5, 4),
            },

            {
                'pk'      : 2,
                'name'    : 'Main Conference',
                'eventOn' : dt.datetime(2025, 5, 5),
                'eventTo' : dt.datetime(2025, 5, 6),
            },
        ]).on_conflict_do_nothing())


if __name__ == '__main__':
    schemas = ['conf25', 'um']
    main(schemas)
