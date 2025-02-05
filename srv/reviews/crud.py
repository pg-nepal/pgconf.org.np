import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.captcha
import srv.auth

from srv import app

@app.get('/reviews')
def review_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(db.proposals.Review)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        review = [row._asdict() for row in cursor]

    return flask.jsonify({
        "review" : review,
        "isAdmin" : isAdmin,
        })

@app.get('/client/reviews')
def client_review_list():

    query = sa.select(db.proposals.Review)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        review = [row._asdict() for row in cursor]

    return flask.jsonify({
        "review" : review,
        })


@app.post('/reviews/add/<int:proposal_pk>')
def review_create(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formdata = flask.request.form.to_dict()

    with db.SessionMaker.begin() as session:
        cursor = session.execute(
            sa.select(
                db.proposals.Proposal.name,
            ).where(
                db.proposals.Proposal.pk == proposal_pk,
            ),
        )

        name = cursor.scalar()

        if not name:
            return flask.jsonify({"error": "Proposal not found"}), 404

        query = sa.insert(
            db.proposals.Review,
            ).values(
                **formdata,
                proposal_pk=proposal_pk,
                createdBy=name,
            )

        session.execute(query)
        return flask.jsonify({
            "success": "Review submitted successfully",
        }), 200


@app.get('/reviews/<int:proposal_pk>')
def review_read(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.proposals.Review,
    ).where(
        db.proposals.Review.proposal_pk == proposal_pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

    if row is None:
        return 'Invalid Pk', 400

    return flask.redirect(
        flask.url_for(),
        proposal = row._asdict(),
        isAdmin  = isAdmin,
    )

@app.get('/client/reviews/<int:proposal_pk>')
def client_review_read(proposal_pk):

    query = sa.select(
        db.proposals.Review,
    ).where(
        db.proposals.Review.proposal_pk == proposal_pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

    if row is None:
        return 'Invalid Pk', 400

    return flask.redirect(
        flask.url_for(),
        proposal = row._asdict(),
    )


@app.post('/reviews/update/<int:pk>')
def review_update(pk):
    data = flask.request.form
    query = sa.update(
        db.proposals.Review,
    ).where(
        db.proposals.Review.pk == pk,
    ).values(
        **data,
        updatedBy = 'dummy',
    )

    with db.Session.begin() as session:
        session.execute(query)
        return flask.redirect(
            flask.url_for(''),
            pk = pk,
        )