import flask
import sqlalchemy as sa

import db
import db.conf
import srv.auth

from srv import app


@app.get('/attendees/form')
def attendee_form():
    return flask.render_template(
        '/attendees/form.djhtml',
    )


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
        db.conf.Attendee.email,
        db.conf.Attendee.category,
        db.conf.Attendee.fee,
        db.conf.Attendee.slug,
        db.conf.Attendee.createdOn,
        sa.cast(db.conf.Attendee.status, sa.String).label('status'),
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.jsonify(
        headers = tuple(c['name'] for c in query.column_descriptions),
        data    = [list(row) for row in cursor],
    )


@app.post('/attendees/add')
def attendee_create():
    formData = flask.request.form
    email = formData.get('email')

    query = sa.insert(
        db.conf.Attendees,
    ).values(
        **formData,
        createdBy = email,
        status    = 'pending',
        ticket    = 'ticket',
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        id = cursor.inserted_primary_key[0]
        return flask.redirect('/attendees/{}'.format(id))


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


@app.delete('/attendees/<int:pk>')
def attendee_delete(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    with db.SessionMaker.begin() as session:
        session.execute(
            sa.delete(
                db.conf.Attendee,
            ).where(
                db.conf.Attendee.pk == pk,
            ),
        )

    return flask.jsonify({
        'msg' : 'Registration deleted successfully',
    }), 202
