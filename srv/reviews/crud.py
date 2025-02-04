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

@app.post('/reviews/add/<int:proposal_pk>')
def review_create(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()


    formdata = flask.request.form.to_dict()
    formdata['proposal_pk'] = proposal_pk
    print("formdata: ",formdata)

    query = sa.insert(
        db.proposals.Review,
        ).values(
            **formdata,
        )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return flask.jsonify({
            "success": "Review submitted successfully",
        }), 200

