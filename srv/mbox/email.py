import flask
import sqlalchemy as sa

import db
import db.mbox
import srv.auth

from srv import app


@app.post('/api/mbox/queue_email')
@srv.auth.auth_required()
def queue_email():
    print('here')
    email_body = flask.render_template (
        'emails/registration_thanks.djhtml',
        name     = "Rupak",
        message  = "message goes here"
    )
    query = sa.insert (
        db.mbox.MBox,
    ).values(
        type = 'email',

        to        = 'rughimire@gmail.com',
        cc        = 'rughimire@gmail.com',

        subject   = 'Hello this is subject',
        body      = email_body,

        createdBy =  srv.auth.loggedInUser(flask.request),
    )

    with db.SessionMaker.begin() as session:
        _ = session.execute(query)
        return flask.jsonify(
            message = "Email Queued for scheduled sending",
        )
