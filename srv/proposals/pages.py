import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.get('/proposals/<int:pk>')
def proposal_read_view(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/proposals/read.djhtml',
        isAdmin = isAdmin,
        pk      = pk,
    )


@app.get('/proposals/accept')
def proposal_accept_view():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/proposals/accept.djhtml',
        pageTitle = 'Accept Proposals',
        pageDesc  = 'List of all submitted proposals',
        baseURL   = '/proposals/accept',
        isAdmin   = isAdmin,
    )


@app.get('/api/proposals/accept')
def proposal_accept_list_api():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Proposal.pk,
        db.programs.Proposal.title,
        sa.func.coalesce(sa.func.round(sa.func.avg(db.programs.Rate.value), 0)).label('avg(rating)'),
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'relevance'), sa.Integer)), 2)).label('Relevance'),
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'clarity'), sa.Integer)), 2)).label('Clarity'),
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'engagement'), sa.Integer)), 2)).label('Engagemenet'),
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'content'), sa.Integer)), 2)).label('Content'),
        sa.func.count(db.programs.Rate.proposal_pk).label('Rated by'),
        db.programs.Proposal.status.label('Status'),
        sa.literal(None).label('Action'),
    ).outerjoin(
        db.programs.Rate,
        db.programs.Proposal.pk == db.programs.Rate.proposal_pk,
    ).group_by(
        db.programs.Proposal.pk,
    ).order_by(
        db.programs.Proposal.pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [ list(row) for row in cursor ],
        )


@app.get('/proposals/accept/<int:pk>')
def proposal_accept(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.update(
        db.programs.Proposal,
    ).where(
        db.programs.Proposal.pk == pk,
    ).values(
        status      = 'accepted',
        updatedBy   = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return "Proposal accepted"
