import flask
import sqlalchemy as sa

import db
import db.conf
import uploads

from srv import app


@app.get('/registered/<slug>')
def registered_read(slug):
    query = sa.select(
        db.conf.Attendee.name,
        db.conf.Attendee.email,
        db.conf.Attendee.country,
        db.conf.Attendee.fee,
        db.conf.Attendee.slug,
        db.conf.Attendee.receiptPath,
        sa.cast(db.conf.Attendee.status, sa.String).label('status'),
    ).where(
        sa.cast(db.conf.Attendee.slug, sa.String) == slug,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid uuid', 400

        return flask.render_template(
            '/attendees/profile.djhtml',
            row = row._asdict(),
        )


@app.post('/registered/<slug>')
def registered_update(slug):
    fileData = flask.request.files

    fullpath = uploads.save(fileData, 'receiptPath')

    query = sa.update(
        db.conf.Attendee,
    ).where(
        sa.cast(db.conf.Attendee.slug, sa.String) == slug,
    ).values(
        receiptPath = fullpath,
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400
