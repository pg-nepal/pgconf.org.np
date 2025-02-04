import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.get('/api/review/mine/list/<int:proposal_pk>')
def review_list_mine(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Review.pk,
        db.programs.Review.comment,
        db.programs.Review.createdBy,
        db.programs.Review.createdOn,
    ).where(
        db.programs.Review.proposal_pk == proposal_pk,
        db.programs.Review.createdBy   == isAdmin,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify([list(row) for row in cursor])
