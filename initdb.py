#!venv/bin/python

import sqlalchemy as sa

import db
import db.conf
import db.programs


def main(schemas):
    with db.engine.begin() as conn:
        for schema in schemas:
            conn.execute(sa.text('CREATE SCHEMA IF NOT EXISTS {}'.format(schema))) # noqa: E501

    db.meta.create_all(bind=db.engine, checkfirst=True)


if __name__ == '__main__':
    schemas = ['conf25', 'um']
    main(schemas)
