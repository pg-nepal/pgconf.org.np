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


@app.get('/ratings/<int:proposal_pk>')
def rating_read(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    print('isadmin: ', isAdmin)

    query = sa.select(
        db.proposals.Rating,
    ).where(
        db.proposals.Rating.proposal_pk == proposal_pk,
        db.proposals.Rating.createdBy == isAdmin,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return flask.jsonify({
                "message": "You haven't rated this proposal.",
            })

        return flask.jsonify(dict(row._mapping))
        

@app.post('/rating/<int:proposal_pk>')
def rating_update(proposal_pk):
    
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
        updatedBy=isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return flask.jsonify({
            "success": "Ratings updated successfully",
        }), 200