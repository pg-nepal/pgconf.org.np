import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.get('/api/rates/mine/list/<int:proposal_pk>')
def rate_list_mine(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.Programs.Rate,
    ).where(
        db.programs.Rate.proposal_pk == proposal_pk,
        db.programs.Rate.createdBy == isAdmin,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        return flask.jsonify(
            [list(row) for row in cursor],
        )


@app.get('/api/rates/mine/<int:proposal_pk>')
def rate_read_mine(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Rate.value,
        db.programs.Rate.score,
    ).where(
        db.programs.Rate.proposal_pk == proposal_pk,
        db.programs.Rate.createdBy   == isAdmin,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()
        if row is None:
            return flask.jsonify({})
        return flask.jsonify(row._asdict())


@app.post('/api/rates/mine/<int:proposal_pk>')
def rate_update_or_insert(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    jsonData = flask.request.json

    with db.SessionMaker.begin() as session:
        cursor = session.execute(sa.update(
            db.programs.Rate,
        ).where(
            db.programs.Rate.proposal_pk == proposal_pk,
            db.programs.Rate.createdBy   == isAdmin,
        ).values(
            **jsonData,
            updatedBy = isAdmin,
        ))

        if cursor.rowcount > 0:
            return 'Rating updated successfully', 202

        session.execute(sa.insert(
            db.programs.Rate,
        ).values(
            **jsonData,
            proposal_pk = proposal_pk,
            createdBy   = isAdmin,
            updatedBy   = isAdmin,
        ))
        return 'Ratings created successfully', 201


@app.get('/api/rates/summary/<int:proposal_pk>')
def rate_summary(proposal_pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()
@app.get('/api/submitted/rates/summary/<int:proposal_pk>')
def client_rating_summary(proposal_pk):
    return rating_summary(proposal_pk)

def rating_summary(proposal_pk):

    count = sa.func.count(db.programs.Rate.pk)
    avg   = sa.func.avg(db.programs.Rate.value)

    query = sa.select(
        count.label('count'),
        avg.label('avg'),
        sa.func.round(avg / 5 * 100, 2).label('percent'),
    ).where(
        db.programs.Rate.proposal_pk == proposal_pk,
    )

    with db.engine.connect() as connection:
        row = connection.execute(query).first()
        return flask.jsonify(row._asdict())
