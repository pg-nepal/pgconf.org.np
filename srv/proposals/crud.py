import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.auth

from srv import app
# from flask_jwt_extended import jwt_required, get_jwt_identity


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

    query = sa.select(db.proposals.Proposals)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        '/proposals/list.djhtml',
        cursor  = cursor,
        isAdmin = isAdmin,
    )


@app.post('/proposals/add')
# @jwt_required()
def proposal_create():
    formdata = flask.request.form.to_dict()

    query = sa.insert(
        db.proposals.Proposals
    ).values(
        **formdata
    )

    with db.Session.begin() as session:
        session.execute(query)

    return flask.redirect('/call_for_proposal')


@app.get('/proposals/<int:pk>')
def proposal_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.proposals.Proposals,
    ).where(
        db.proposals.Proposals.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

    if row is None:
        return 'Invalid Pk', 400

    return flask.render_template(
        '/proposals/read.djhtml',
        proposal = row._asdict(),
        isAdmin  = isAdmin,
    )


@app.delete('/proposals/<int:pk>')
def proposal_delete(pk):
    with db.Session.begin() as session:
        session.execute(sa.delete(
            db.proposals.Proposals,
        ).where(
            db.proposals.Proposals.pk==pk,
        ))

    return flask.jsonify({
        'message' : 'Proposal deleted successfully'
    }), 202
