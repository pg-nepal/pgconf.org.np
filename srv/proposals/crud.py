import random

import flask
import sqlalchemy as sa

import db
import db.programs
import srv.captcha
import srv.auth

from srv import app


@app.get('/proposals/form')
def proposal_form():
    idx = random.randrange(len(srv.captcha.questions))  # noqa:S311
    return flask.render_template(
        '/proposals/form.djhtml',
        idx      = idx,
        question = srv.captcha.questions[idx][0],
    )


@app.get('/proposals')
def proposal_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/table.djhtml',
        pageTitle = 'Proposals',
        pageDesc  = 'List of all submitted proposals',
        baseURL   = '/proposals',
        isAdmin   = isAdmin,
    )


@app.get('/api/proposals')
def proposal_list_api():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Proposal.pk,
        db.programs.Proposal.title,
        db.programs.Proposal.name,
        db.programs.Proposal.createdOn,
        sa.func.coalesce(sa.func.round(sa.func.avg(db.programs.Rate.value), 0)).label('avg(rating)'),  # noqa:E501
    ).outerjoin(
        db.programs.Rate,
        db.programs.Proposal.pk == db.programs.Rate.proposal_pk,
    ).group_by(
        db.programs.Proposal.pk,
    ).order_by(
        db.programs.Proposal.pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [ list(row) for row in cursor ],
        )


@app.post('/proposals/add')
def proposal_create():
    formData = flask.request.form.to_dict()
    email = formData['email']

    idx = int(formData.pop('idx'))
    answer = formData.pop('answer').upper()

    if answer != srv.captcha.questions[idx][1]:
        return 'Incorrect answer', 400

    query = sa.insert(
        db.programs.Proposal,
    ).values(
        **formData,
        createdBy = email,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)

    return flask.redirect('/pages/call-for-proposal')


@app.get('/api/proposals/<int:pk>')
def proposal_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Proposal.pk,

        db.programs.Proposal.title,
        db.programs.Proposal.abstract,

        db.programs.Proposal.name,
        db.programs.Proposal.email,
        db.programs.Proposal.country,
        db.programs.Proposal.createdOn,
        db.programs.Proposal.session,
    ).where(
        db.programs.Proposal.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid Pk', 400

        return flask.jsonify(row._asdict())


@app.get('/proposals/action/<int:pk>')
def proposal_action(pk):
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
            '/proposals/action.djhtml',
            row     = row,
            isAdmin = isAdmin,
        )


@app.post('/proposals/<int:pk>')
def proposal_update(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    data = flask.request.form
    query = sa.update(
        db.programs.Proposal,
    ).where(
        db.programs.Proposal.pk == pk,
    ).values(
        **data,
        updatedBy = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return flask.redirect('/proposals'), 202


@app.delete('/proposals/<int:pk>')
def proposal_delete(pk):
    return 'Sorry, Proposal can not be deleted at this moment', 202

    with db.SessionMaker.begin() as session:
        session.execute(sa.delete(
            db.programs.Proposal,
        ).where(
            db.programs.Proposal.pk == pk,
        ))
