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
    ).returning(
        db.programs.Proposal.pk,
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)

        emailBody = flask.render_template (
            '/emails/cfp_thanks.djhtml',
            name      = formData['name'],
            email     = email,
            title     = formData['title'],
            session   = formData['session'],
            abstract  = formData['abstract'],
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
