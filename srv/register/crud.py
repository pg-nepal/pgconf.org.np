import flask
import sqlalchemy as sa

import db
import db.events
import srv.auth

from srv import app


@app.get('/register/form')
def register_form():
    return flask.render_template(
        '/register/form.djhtml'
    )


@app.get('/register')
def register_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(db.registrations.Registrations)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        '/register/list.djhtml',
        cursor  = cursor,
        isAdmin = isAdmin
    )


@app.post('/register/add')
def register_create():
    formdata = flask.request.form.to_dict()

    query = sa.insert(
        db.events.Register
    ).values(
        **formdata,
        fee    = 1000,
        status = 'pending',
        ticket = 'ticket',
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return flask.redirect('/register')


@app.get('/register/<int:pk>')
def register_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.events.Register,
    ).where(
        db.events.Register.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid pk', 400

        return flask.render_template(
            '/register/read.djhtml',
            row     = row,
            isAdmin = isAdmin,
        )


@app.delete('/registrations/<int:pk>')
def register_delete(pk):
    with db.SessionMake.begin() as session:
        session.execute(
            sa.delete(
                db.events.Register,
            ).where(
                db.events.Register.pk == pk,
            )
        )

    return flask.jsonify({
        'message': 'Registration deleted successfully'
    }), 202
