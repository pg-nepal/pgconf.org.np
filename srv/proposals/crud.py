import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.get('/proposals/form')
def proposal_form():
    return flask.render_template(
        '/proposals/form.djhtml',
    )


@app.get('/proposals')
def proposal_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/table.djhtml',
        pageTitle = 'Proposals',
        pageDesc  = 'List of all submitted proposals',
        baseURL   = '/proposals',
        isAdmin   = isAdmin,
    )


@app.post('/api/proposals')
def proposal_list_api():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    jsonData = flask.request.json

    query = sa.select(
        db.programs.Proposal.pk,
        db.programs.Proposal.title,
        db.programs.Proposal.name,
        db.programs.Proposal.country,
        db.programs.Proposal.session,
        db.programs.Proposal.createdOn,
        sa.cast(db.programs.Proposal.status, sa.String),
        sa.func.coalesce(sa.func.round(sa.func.avg(db.programs.Rate.value), 0)).label('avg(rating)'),  # noqa:E501
    ).outerjoin(
        db.programs.Rate,
        db.programs.Proposal.pk == db.programs.Rate.proposal_pk,
    ).group_by(
        db.programs.Proposal.pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query.where(*[
            c['expr'] == jsonData['filter'][c['name']]
            for c in query.column_descriptions
            if jsonData['filter'].get(c['name'], 'all') != 'all'
        ]).order_by(
            db.conf.Attendee.pk,
        ))

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [ list(row) for row in cursor ],
            filters = {
                'session' : ('all', 'talk', 'workshop', 'keynote'),
                'status'  : ('all', *db.programs.proposal_status),
            },
        )


@app.post('/proposals/add')
def proposal_create():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formData = flask.request.form

    query = sa.insert(
        db.programs.Proposal,
    ).values(
        **formData,
        createdBy = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return flask.redirect('/pages/call-for-proposal')


@app.get('/api/proposals/<int:pk>')
def proposal_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Proposal.pk,

        db.programs.Proposal.title,
        db.programs.Proposal.abstract,

        db.programs.Proposal.name,
        db.programs.Proposal.email,
        db.programs.Proposal.country,
        db.programs.Proposal.createdOn,
        db.programs.Proposal.session,
    ).where(
        db.programs.Proposal.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid Pk', 400

        return flask.jsonify(row._asdict())


@app.post('/proposals/<int:pk>')
def proposal_update(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formData = flask.request.form

    query = sa.update(
        db.programs.Proposal,
    ).where(
        db.programs.Proposal.pk == pk,
    ).values(
        **formData,
        updatedBy = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return flask.redirect('/proposals'), 202
