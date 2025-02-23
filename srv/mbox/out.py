import flask
import sqlalchemy as sa

import db
import db.mbox
import srv.auth


def queue(ref, to, cc, subject, body, type='email', note=None):
    query = sa.insert (
        db.mbox.MBox,
    ).values(
        type      = type,
        ref       = ref,
        to        = to,
        cc        = cc if cc != '' else None,
        subject   = subject,
        body      = body,
        note      = note,
        createdBy = srv.auth.loggedInUser(flask.request),
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return True, {
            'message' : 'Email Queued for scheduled sending',
        }
