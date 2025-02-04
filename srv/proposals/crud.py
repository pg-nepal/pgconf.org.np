import random

import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.captcha
import srv.auth

from srv import app


@app.get('/proposals/form')
def proposal_form():
    idx = random.randrange(len(srv.captcha.questions))  # noqa:S311
    return flask.render_template(
        '/proposals/form.djhtml',
        idx      = idx,
        question = srv.captcha.questions[idx][0],
    )


@app.get('/proposals')
def proposal_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.proposals.Proposal,
        sa.func.coalesce(sa.func.round(sa.func.avg(db.proposals.Review.rating), 0)).label("average_rating"),
        ).outerjoin(
            db.proposals.Review, db.proposals.Proposal.pk == db.proposals.Review.proposal_pk,
        ).where(
            db.proposals.Proposal.rec_status=='A'
        ).group_by(
            db.proposals.Proposal.pk,
        ).order_by(
            sa.desc("average_rating"),
        )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        '/proposals/list.djhtml',
        cursor  = cursor,
        isAdmin = isAdmin,
    )


@app.get('/client/proposals')
def client_proposal_list():

    query = sa.select(
        db.proposals.Proposal,
        sa.func.coalesce(sa.func.round(sa.func.avg(db.proposals.Review.rating), 0)).label("average_rating"),
        ).outerjoin(
            db.proposals.Review, db.proposals.Proposal.pk == db.proposals.Review.proposal_pk
        ).group_by(
            db.proposals.Proposal.pk
        ).order_by(
            sa.desc("average_rating").nulls_last(),
        )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        '/proposals/list.djhtml',
        cursor  = cursor,
    )    


@app.post('/proposals/add')
def proposal_create():
    formData = flask.request.form.to_dict()

    idx = int(formData.pop('idx'))
    answer = formData.pop('answer').upper()

    if answer != srv.captcha.questions[idx][1]:
        return 'Incorrect answer', 400

    query = sa.insert(
        db.proposals.Proposal,
    ).values(
        **formData,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)

    return flask.redirect('/pages/call-for-proposal')


@app.get('/proposals/<int:pk>')
def proposal_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.proposals.Proposal,
    ).where(
        db.proposals.Proposal.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

    if row is None:
        return 'Invalid proposal Pk', 400

    review_query = sa.select(
        db.proposals.Review,
    ).where(
        db.proposals.Review.proposal_pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(review_query)
        reviews = cursor.fetchall()
        print (reviews)

    return flask.render_template(
        '/proposals/read.djhtml',
        proposal = row._asdict(),
        review = [review._asdict() for review in reviews],
        isAdmin  = isAdmin,
    )


@app.get('/client/proposals/<int:pk>')
def client_proposal_read(pk):

    query = sa.select(
        db.proposals.Proposal,
    ).where(
        db.proposals.Proposal.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

    if row is None:
        return 'Invalid proposal Pk', 400

    review_query = sa.select(
        db.proposals.Review,
    ).where(
        db.proposals.Review.proposal_pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(review_query)
        reviews = cursor.fetchall()
        print (reviews)

    return flask.render_template(
        '/proposals/read.djhtml',
        proposal = row._asdict(),
        review = [review._asdict() for review in reviews],
    )


@app.post('/proposals/<int:pk>')
def proposal_update(pk):
    data = flask.request.form
    query = sa.update(
        db.proposals.Proposal,
    ).where(
        db.proposals.Proposal.pk == pk,
    ).values(
        **data,
        updatedBy = 'dummy',
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return flask.redirect(
            flask.url_for('proposal_read'),
            pk = pk,
        )


@app.delete('/proposals/<int:pk>')
def proposal_delete(pk):
    # with db.SessionMaker.begin() as session:
    #     session.execute(sa.delete(
    #         db.proposals.Proposal,
    #     ).where(
    #         db.proposals.Proposal.pk == pk,
    #     ))

    return 'Sorry, Proposal can not be deleted at this moment', 202
