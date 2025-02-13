import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.auth

from srv import app


@app.get('/api/proposals/review/<int:pk>')
def proposal_review_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.proposals.Review,
    ).where(
        db.proposals.Review.proposal_pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        return flask.jsonify(
            [ row._asdict() for row in cursor ],
        )
