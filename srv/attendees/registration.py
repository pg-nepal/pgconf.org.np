import flask
import sqlalchemy as sa

import db
import db.events

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
