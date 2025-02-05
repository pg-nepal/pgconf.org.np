import random

import flask
import sqlalchemy as sa

import db
import db.programs
import srv.captcha

from srv import app


@app.get('/proposals/call/form')
def proposal_call_form():
    idx = random.randrange(len(srv.captcha.questions))  # noqa:S311
    return flask.render_template(
        '/proposals/form.djhtml',
        idx      = idx,
        question = srv.captcha.questions[idx][0],
    )


@app.post('/proposals/call/add')
def proposal_call_create():
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
