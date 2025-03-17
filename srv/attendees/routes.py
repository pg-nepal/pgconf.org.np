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


@app.post('/api/attendees/filter')
def attendee_filter():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    json = flask.request.json

    query = sa.select(
        db.conf.Attendee.pk,
        db.conf.Attendee.name,
        db.conf.Attendee.email,
        db.conf.Attendee.category,
        sa.cast(db.conf.Attendee.type, sa.String).label('type'),
        db.conf.Attendee.createdOn,
        sa.cast(db.conf.Attendee.status, sa.String).label('status'),
    )

    if(json['category'] != 'all'):
        query = query.where(db.conf.Attendee.category == json['category'])

    if(json['type'] != 'all'):
        query = query.where(db.conf.Attendee.type == json['type'])

    if(json['status'] != 'all'):
        query = query.where(db.conf.Attendee.status == json['status'])

    query = query.order_by(db.conf.Attendee.pk)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [ list(row) for row in cursor ],
        )
