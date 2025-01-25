import flask
import sqlalchemy as sa

import db
import db.events
import uploads

from srv import app


@app.get('/registered/<slug>')
def registered_read_client(slug):
    query = sa.select(
        db.events.Attendee,
    ).where(
        db.events.Attendee.slug == slug.encode(),
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid uuid', 400

        data = dict(row._mapping)

        if data.get('slug'):
            data['slug'] = data['slug'].decode()

        return flask.render_template(
            '/attendees/profile.djhtml',
            row = data,
        )


@app.post('/registered/<slug>')
def registered_update(slug):
    fileData = flask.request.files

    fullpath = uploads.save(fileData, 'receipt_url')

    query = sa.update(
        db.events.Attendee,
    ).where(
        db.events.Attendee.slug == slug.encode(),
    ).values(
        receipt_url = fullpath,
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400
