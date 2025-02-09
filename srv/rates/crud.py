import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.auth

from srv import app


@app.get('/api/rates')
def rate_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid

    query = sa.select(
        db.proposals.Rate.proposal_pk,
        db.proposals.Rate.value,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [list(row) for row in cursor],
        )


@app.post('/api/rates/add/<int:proposal_pk>')
def rate_create(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formData = flask.request.form

    with db.SessionMaker.begin() as session:
        row = session.execute(
            sa.select(
                db.proposals.Proposal.pk,
            ).where(
                db.proposals.Proposal.pk == proposal_pk,
            ),
        ).first()

        if row is None:
            return 'Invalid Pk', 400

        session.execute(sa.insert(
            db.proposals.Rate,
        ).values(
            **formData,
            proposal_pk = proposal_pk,
            createdBy   = isAdmin,
        ))

        return 'Rating submitted successfully'


@app.get('/rates/<int:proposal_pk>')
def rate_read(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.proposals.Rate.proposal_pk,
        db.proposals.Rate.value,
    ).where(
        db.proposals.Rate.proposal_pk == proposal_pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [list(row) for row in cursor],
        )
        # return flask.jsonify(dict(row._mapping))


@app.post('/rates/<int:proposal_pk>')
def rate_update(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formdata = flask.request.form

    query = sa.update(
        db.proposals.Rating,
    ).where(
        db.proposals.Rating.proposal_pk == proposal_pk,
        db.proposals.Rating.createdBy == isAdmin,
    ).values(
        **formdata,
        updatedBy = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return 'Ratings updated successfully', 202
