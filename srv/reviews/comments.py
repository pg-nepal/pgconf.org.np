import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.get('/api/reviews/mine/<int:proposal_pk>')
def review_read_mine(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Review.pk,
        db.programs.Review.comment,
        db.programs.Review.updatedOn,
        db.programs.Review.createdBy,
    ).where(
        db.programs.Review.proposal_pk == proposal_pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [list(row) for row in cursor],
        )


@app.delete('/api/reviews/mine/delete/<int:pk>')
def review_delete_mine(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    with db.SessionMaker.begin() as session:

        session.execute(sa.delete(
            db.programs.Review,
        ).where(
            db.programs.Review.pk == pk,
            db.programs.Review.createdBy == isAdmin,
        ))
        
        return 'Comment deleted successfully', 200