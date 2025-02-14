import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.auth

from srv import app


@app.get('/api/reviews/mine/<int:proposal_pk>')
def review_read_mine(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.proposals.Review.comment,
        db.proposals.Review.updatedOn,
    ).where(
        db.proposals.Review.proposal_pk == proposal_pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [list(row) for row in cursor],
        )
