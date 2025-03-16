import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.get('/proposals/<int:pk>')
def proposal_read_view(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/proposals/read.djhtml',
        isAdmin = isAdmin,
        pk      = pk,
    )


@app.get('/proposals/evaluation')
def proposal_evaluation_view():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/proposals/evaluation.djhtml',
        pageTitle = 'Evaluate Proposals',
        pageDesc  = 'List of all submitted proposals',
        baseURL   = '/proposals/evaluation',
        isAdmin   = isAdmin,
    )
