import flask
import sqlalchemy as sa

import db
import db.events

from srv import app


@app.get('/attendees/<slug>')
def attendee_read_client(slug):
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
