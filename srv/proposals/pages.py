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
        '/proposals/evaluation.djhtml',
        pageTitle = 'Evaluate Proposals',
        pageDesc  = 'List of all submitted proposals',
        baseURL   = '/proposals/evaluation',
        isAdmin   = isAdmin,
    )


@app.post('/api/proposals/evaluation')
def proposal_evaluation_list_api():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    jsonData = flask.request.json

    query = sa.select(
        db.programs.Proposal.pk,
        db.programs.Proposal.title,
        sa.func.coalesce(sa.func.round(sa.func.avg(db.programs.Rate.value), 0)).label('avg(rating)'),  # noqa:E501
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'relevance'), sa.Integer)), 2)).label('Relevance'),  # noqa:E501
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'clarity'), sa.Integer)), 2)).label('Clarity'),  # noqa:E501
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'engagement'), sa.Integer)), 2)).label('Engagement'),  # noqa:E501
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'content'), sa.Integer)), 2)).label('Content'),  # noqa:E501
        sa.func.count(db.programs.Rate.proposal_pk).label('Rated by'),
        sa.cast(db.programs.Proposal.status, sa.String),
        db.programs.Proposal.status.label('Action'),
    ).outerjoin(
        db.programs.Rate,
        db.programs.Proposal.pk == db.programs.Rate.proposal_pk,
    ).group_by(
        db.programs.Proposal.pk,
    ).order_by(
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
                'status' : ('all', *db.programs.proposal_status),
            },
        )
