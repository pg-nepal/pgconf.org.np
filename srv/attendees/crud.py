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
            show    = {
                'Name'          : row.name,
                'Email'         : row.email,
                'Country'       : row.country,
                'Registered On' : row.createdOn.strftime('%B %d %Y'),
                'Category'      : row.category,
            },
        )


@app.post('/attendees/<int:pk>')
def attendee_update(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    file_photoBlob = flask.request.files['photoBlob']

    if file_photoBlob is None:
        return 'File not uploaded', 400

    with db.SessionMaker.begin() as session:
        cursor = session.execute(sa.update(
            db.conf.Attendee,
        ).where(
            db.conf.Attendee.pk == pk,
        ).values(
            photoBlob     = file_photoBlob.read(),
            photoMime     = file_photoBlob.content_type,
        ))
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400
