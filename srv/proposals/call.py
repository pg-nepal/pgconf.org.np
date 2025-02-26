import random

import flask
import sqlalchemy as sa

import db
import db.programs
import srv.captcha
import srv.mbox.out

from srv import app


@app.get('/proposals/call/form')
def proposal_call_form():
    idx = random.randrange(len(srv.captcha.questions))  # noqa:S311
    return flask.render_template(
        '/form-captcha.djhtml',
        pageTitle = '/ Call for Proposal',
        fields    = '/proposals/form-part.djhtml',
        script    = '/static/proposals/form.mjs',
        question  = srv.captcha.questions[idx][0],
        idx       = idx,
    )

    return flask.render_template(
        '/proposals/form.djhtml',
        idx      = idx,
        question = srv.captcha.questions[idx][0],
    )


@app.post('/proposals/call/add')
def proposal_call_create():
    jsonData = flask.request.json
    email = jsonData['email']

    idx = jsonData.pop('idx')
    answer = jsonData.pop('answer').upper()
    if answer != srv.captcha.questions[idx][1]:
        return 'Incorrect answer', 400

    query = sa.insert(
        db.programs.Proposal,
    ).values(
        **jsonData,
        createdBy = email,
    ).returning(
        db.programs.Proposal.pk,
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)

        emailBody = flask.render_template (
            '/emails/cfp_thanks.djhtml',
            name      = jsonData['name'],
            email     = email,
            title     = jsonData['title'],
            session   = jsonData['session'],
            abstract  = jsonData['abstract'],
        )

        srv.mbox.out.queue(
            ref     = cursor.scalar(),
            to      = email,
            cc      = None,
            subject = 'Thank You for submitting the proposal',
            body    = emailBody,
            note    = 'talk submission',
        )

        return flask.redirect('/pages/call-for-proposal')
