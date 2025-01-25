import flask
import sqlalchemy as sa

import db
import db.events
import uploads

from srv import app


@app.get('/registered/<slug>')
def registered_read(slug):
    query = sa.select(
        db.events.Attendee.name,
        db.events.Attendee.email,
        db.events.Attendee.country,
        db.events.Attendee.fee,
        db.events.Attendee.slug,
        db.events.Attendee.receiptPath,
        sa.cast(db.events.Attendee.status, sa.String).label('status'),
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
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
        db.events.Attendee,
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
    ).values(
        receiptPath = fullpath,
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400
