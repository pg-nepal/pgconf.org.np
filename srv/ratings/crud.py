import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.auth

from srv import app

@app.post('/rating')
def rating_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid

    query = sa.select(db.proposals.Rating)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        rating = [cursor._asdict() for row in cursor]

    return flask.jsonify({
        "rating"  : rating,
        "isAdmin" : isAdmin,
    })


@app.post('/rating/add/<int:proposal_pk>')
def rating_create(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formdata = flask.request.form.to_dict()

    with db.SessionMaker.begin() as session:

        cursor = session.execute(
            sa.select(
                db.proposals.Proposal,
            ).where(
                db.proposals.Proposal.pk == proposal_pk,
            ),
        )

        proposal = cursor.scalar()

        if not proposal:
            return flask.jsonify({
                "error" : "Proposal not found",
            }), 404

        query = sa.insert(
            db.proposals.Rating,
            ).values(
                **formdata,
                proposal_pk=proposal_pk,
                createdBy=isAdmin,
            )

        session.execute(query)
        return flask.jsonify({
            "success": "Rating submitted successfully",
        }), 200
