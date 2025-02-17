import flask
import sqlalchemy as sa

import db
import db.programs
import srv.captcha
import srv.auth

from srv import app


@app.get('/reviews')
def review_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(db.programs.Review)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify({
            'data' : [list(row) for row in cursor],
        })


@app.post('/reviews/add/<int:proposal_pk>')
def review_create(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formData = flask.request.form

    query = sa.insert(
        db.programs.Review,
    ).values(
        **formData,
        proposal_pk = proposal_pk,
        createdBy   = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return 'Review submitted successfully'


@app.get('/reviews/<int:proposal_pk>')
def review_read(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Review,
    ).where(
        db.programs.Review.proposal_pk == proposal_pk,
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
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    data = flask.request.form
    query = sa.update(
        db.programs.Review,
    ).where(
        db.programs.Review.pk == pk,
    ).values(
        **data,
        updatedBy = isAdmin,
    )

    with db.Session.begin() as session:
        session.execute(query)

        return flask.redirect(
            flask.url_for(''),
            pk = pk,
        )


@app.delete('/reviews/delete/<int:pk>')
def review_delete(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    with db.SessionMaker.begin() as session:
        session.execute(
            sa.delete(
                db.programs.Review,
            ).where(
                db.programs.Review.pk == pk,

            ),
        )

        return 'Review deleted successfully', 202
