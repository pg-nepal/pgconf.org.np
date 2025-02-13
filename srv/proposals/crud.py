import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.get('/proposals/form')
def proposal_page_form():
    return flask.render_template(
        '/proposals/form.djhtml',
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


@app.post('/api/proposals/add')
def proposal_create():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formData = flask.request.form

    query = sa.insert(
        db.programs.Proposal,
    ).values(
        **formData,
        createdBy = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return flask.redirect('/pages/call-for-proposal')


@app.get('/proposals/<int:pk>')
def proposal_page_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/proposals/read.djhtml',
        isAdmin = isAdmin,
        pk      = pk,
        status  = db.programs.proposal_status,
    )


@app.post('/api/proposals/<int:pk>')
def proposal_update(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formData = flask.request.form.to_dict()
    name = formData.get('name') or isAdmin

    query = sa.update(
        db.programs.Proposal,
    ).where(
        db.programs.Proposal.pk == pk,
    ).values(
        **formData,
        updatedBy = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return flask.redirect('/proposals'), 202
