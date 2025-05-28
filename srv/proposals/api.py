import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.post('/api/proposals/update/<int:pk>')
def proposal_attendee_pk_update(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    updated_values = {
        'updatedBy' : isAdmin,
    }

    jsonData = flask.request.json
    attendee_pk = jsonData.pop('attendeePk')

    if attendee_pk is not None:
        updated_values['attendee_pk'] = attendee_pk

    query = sa.update(
        db.programs.Proposal,
    ).where(
        db.programs.Proposal.pk == pk,
    ).values(
        **updated_values,
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        return 'Updated Row',200 if cursor.rowcount > 0 else 400

