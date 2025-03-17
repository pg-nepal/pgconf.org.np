import io

import flask
import sqlalchemy as sa

import db
import srv.auth

from srv import app


@app.route('/attendees/<int:pk>.photo')
@srv.auth.auth_required()
def attendee_read_photo(pk):
    query = sa.select(
        db.conf.Attendee.photoBlob,
        db.conf.Attendee.photoMime,
    ).where(
        db.conf.Attendee.pk == pk,
    )

    with db.engine.connect() as connection:
        row = connection.execute(query).first()

        if row is None:
            return 'File Not Found', 404

        return flask.send_file(
            io.BytesIO(row.photoBlob),
            mimetype = row.photoMime or 'image/png',
        )
