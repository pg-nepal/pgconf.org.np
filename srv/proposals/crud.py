import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.get('/proposals/form')
def proposal_form():
    return flask.render_template(
        '/proposals/form.djhtml',
    )


@app.get('/proposals')
def proposal_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(db.programs.Proposal)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.render_template(
            '/proposals/list.djhtml',
            cursor  = cursor,
            isAdmin = isAdmin,
        )


@app.post('/proposals/add')
def proposal_create():
    formData = flask.request.form.to_dict()

    query = sa.insert(
        db.programs.Proposal,
    ).values(
        **formData,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)

    return flask.redirect('/pages/call-for-proposal')


@app.get('/proposals/<int:pk>')
def proposal_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Proposal,
    ).where(
        db.programs.Proposal.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid Pk', 400

        return flask.render_template(
            '/proposals/read.djhtml',
            row     = row,
            isAdmin = isAdmin,
        )
