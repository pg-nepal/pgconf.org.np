import flask
import sqlalchemy as sa

import db
import db.conf
import srv.auth

from srv import app


@app.get('/attendees')
def attendee_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/table.djhtml',
        pageTitle = 'Attendees',
        pageDesc  = 'List of all registered attendees',
        baseURL   = '/attendees',
        isAdmin   = isAdmin,
    )


@app.get('/api/attendees')
def attendee_list_api():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.conf.Attendee.pk,
        db.conf.Attendee.name,
        db.conf.Attendee.country,
        db.conf.Attendee.category,
        sa.cast(db.conf.Attendee.type, sa.String).label('type'),
        db.conf.Attendee.createdOn,
        sa.cast(db.conf.Attendee.status, sa.String).label('status'),
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.jsonify(
        headers = tuple(c['name'] for c in query.column_descriptions),
        data    = [list(row) for row in cursor],
    )


@app.get('/attendees/<int:pk>')
@srv.auth.auth_required()
def attendee_read(pk):
    query = sa.select(
        db.conf.Attendee,
    ).where(
        db.conf.Attendee.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid pk', 400

        return flask.render_template(
            '/attendees/read.djhtml',
            isAdmin = srv.auth.loggedInUser(flask.request),
            row     = row,
        )
