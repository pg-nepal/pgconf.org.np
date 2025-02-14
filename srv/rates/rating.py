import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.auth

from srv import app


@app.get('/api/rates/mine/<int:proposal_pk>')
def rate_read_mine(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.proposals.Rate.value,
    ).where(
        db.proposals.Rate.proposal_pk == proposal_pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()
        return flask.jsonify(row and row.value)


@app.post('/api/rates/mine/<int:proposal_pk>')
def rate_update_or_insert(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    with db.SessionMaker.begin() as session:
        cursor = session.execute(sa.update(
            db.proposals.Rate,
        ).where(
            db.proposals.Rate.proposal_pk == proposal_pk,
            db.proposals.Rate.createdBy   == isAdmin,
        ).values(
            value     = flask.request.json['value'],
            updatedBy = isAdmin,
        ))

        if cursor.rowcount > 0:
            return 'Rating updated successfully', 202

        session.execute(sa.insert(
            db.proposals.Rate,
        ).values(
            value       = flask.request.json['value'],
            proposal_pk = proposal_pk,
            createdBy   = isAdmin,
            updatedBy   = isAdmin,
        ))
        return 'Ratings created successfully', 201
