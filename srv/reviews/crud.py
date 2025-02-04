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

