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
