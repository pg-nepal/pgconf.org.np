import flask
import sqlalchemy as sa

import db
import db.events
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

    query = sa.select(
        db.events.Attendee.pk,
        db.events.Attendee.name,
        db.events.Attendee.email,
        db.events.Attendee.category,
        db.events.Attendee.fee,
        db.events.Attendee.slug,
        sa.cast(db.events.Attendee.status, sa.String).label('status'),
        sa.literal(None).label('action'),
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        '/attendees/list.djhtml',
        headers = tuple(c['name'] for c in query.column_descriptions),
        cursor  = cursor,
        isAdmin = isAdmin,
    )


@app.post('/attendees/add')
def attendee_create():
    formData = flask.request.form

    query = sa.insert(
        db.events.Attendees,
    ).values(
        **formData,
        status = 'pending',
        ticket = 'ticket',
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        id = cursor.inserted_primary_key[0]
        return flask.redirect('/attendees/{}'.format(id))


@app.get('/attendees/<int:pk>')
def attendee_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.events.Attendee,
    ).where(
        db.events.Attendee.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid pk', 400

        return flask.render_template(
            '/attendees/read.djhtml',
            row     = row,
            isAdmin = isAdmin,
        )


@app.delete('/attendees/<int:pk>')
def attendee_delete(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()
        
    with db.SessionMaker.begin() as session:
        session.execute(
            sa.delete(
                db.events.Attendee,
            ).where(
                db.events.Attendee.pk == pk,
            ),
        )

    return flask.jsonify({
        'msg' : 'Registration deleted successfully',
    }), 202
