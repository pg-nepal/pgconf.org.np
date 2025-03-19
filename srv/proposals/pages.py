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


@app.get('/proposals/evaluation')
def proposal_evaluation_view():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/table.djhtml',
        pageTitle = 'Evaluate Proposals',
        pageDesc  = 'List of all submitted proposals',
        baseURL   = '/proposals/evaluation',
        isAdmin   = isAdmin,
    )


@app.get('/api/proposals/evaluation')
@app.post('/api/proposals/evaluation')
def proposal_evaluation_list_api():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Proposal.pk,
        db.programs.Proposal.title,
        sa.func.coalesce(sa.func.round(sa.func.avg(db.programs.Rate.value), 0)).label('avg(rating)'),
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'relevance'), sa.Integer)), 2)).label('Relevance'),
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'clarity'), sa.Integer)), 2)).label('Clarity'),
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'engagement'), sa.Integer)), 2)).label('Engagement'),
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'content'), sa.Integer)), 2)).label('Content'),
        sa.func.count(db.programs.Rate.proposal_pk).label('Rated by'),
        sa.cast(db.programs.Proposal.status, sa.String).label('Status'),
        db.programs.Proposal.status.label('Action'),
    ).outerjoin(
        db.programs.Rate,
        db.programs.Proposal.pk == db.programs.Rate.proposal_pk,
    ).group_by(
        db.programs.Proposal.pk,
    ).order_by(
        db.programs.Proposal.pk,
    )

    if flask.request.method == 'POST':
        json = flask.request.json
        if json.get('status') != 'all' and json.get('status') is not None:
            query = query.where(db.programs.Proposal.status == json.get('status'))


    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [ list(row) for row in cursor ],
        )


@app.get('/proposals/evaluation/<int:pk>')
def proposal_evaluation(pk):
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
