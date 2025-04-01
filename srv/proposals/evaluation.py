import flask
import sqlalchemy as sa

import db
import db.programs
import srv.auth

from srv import app


@app.get('/proposals/evaluation/summary')
def evaluation_summary():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/table.djhtml',
        isAdmin   = isAdmin,
        pageTitle = 'Evaluate Proposals',
        pageDesc  = 'List of all submitted proposals',
        baseURL   = '/proposals/evaluation/summary',
        actions   = {
            'pk': {
                'url'    : '/proposals/{pk}',
                'target' : '_blank',
            },
        },
    )


@app.post('/api/proposals/evaluation/summary')
@srv.auth.auth_required()
def proposal_evaluation_summary_api():
    jsonData = flask.request.json

    query = sa.select(
        db.programs.Proposal.pk,
        db.programs.Proposal.title,
        db.programs.Proposal.name,
        db.programs.Proposal.country,
        db.programs.Proposal.session,
        sa.func.count(db.programs.Rate.pk).label('rates'),
        sa.func.coalesce(sa.func.round(sa.func.avg(db.programs.Rate.value), 0)).label('avg(rating)'),  # noqa:E501
    ).outerjoin(
        db.programs.Rate,
        db.programs.Proposal.pk == db.programs.Rate.proposal_pk,
    ).group_by(
        db.programs.Proposal.pk,
    ).order_by(
        sa.nulls_last(sa.desc(sa.func.avg(db.programs.Rate.value)))
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query.where(*[
            c['expr'] == jsonData['filter'][c['name']]
            for c in query.column_descriptions
            if jsonData['filter'].get(c['name'], 'all') != 'all'
        ]).order_by(
            db.programs.Proposal.pk,
        ))

        return flask.jsonify(
            headers = (
                'pk', 'Title', 'Proposed By', 'Country', 'session',
                'No of rates', 'avg(rating)',
            ),
            data    = [ list(row) for row in cursor ],
            filters = {
                'session' : ('all', 'talk', 'workshop', 'keynote'),
            },
        )


@app.get('/proposals/evaluation/report')
def evaluation_report():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Proposal.pk,
        db.programs.Proposal.title,
        db.programs.Proposal.abstract,
        db.programs.Proposal.session,
        db.programs.Proposal.name,
        db.programs.Proposal.createdOn,
    ).order_by(
        db.programs.Proposal.pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        proposal_data = []

        for row in cursor:
            proposal = row._asdict()
            proposal['Rating Details'] = []

            rating_query = sa.select(
                db.programs.Rate.score,
                db.programs.Rate.createdBy,
                db.programs.Rate.value,
            ).filter(
                db.programs.Rate.proposal_pk == proposal['pk'],
            )

            ratings_cursor = connection.execute(rating_query)
            for rating in ratings_cursor:
                proposal['Rating Details'].append(rating._asdict())

            proposal_data.append(proposal)

        return flask.render_template(
            '/proposals/evaluation_report.djhtml',
            isAdmin   = isAdmin,
            pageTitle = 'Proposal Evaluation',
            pageDesc  = 'Detailed report of proposal evaluation',
            baseURL   = '/proposals',
            data      = proposal_data,
        )


@app.get('/api/proposals/evaluation/<slug>')
def submitted_evaluation_mine(slug):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.programs.Proposal.title,
        sa.func.coalesce(sa.func.round(sa.func.avg(db.programs.Rate.value), 0)).label('avg(rating)'),  # noqa:E501
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'relevance'), sa.Integer)), 2)).label('Relevance'),  # noqa:E501
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'clarity'), sa.Integer)), 2)).label('Clarity'),  # noqa:E501
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'engagement'), sa.Integer)), 2)).label('Engagement'),  # noqa:E501
        sa.func.coalesce(sa.func.round(sa.func.avg(sa.func.cast(sa.func.json_extract_path_text(db.programs.Rate.score, 'content'), sa.Integer)), 2)).label('Content'),  # noqa:E501
        sa.func.count(db.programs.Rate.proposal_pk).label('Rated by'),
        sa.cast(db.programs.Proposal.status, sa.String),
    ).outerjoin(
        db.programs.Rate,
        db.programs.Proposal.pk == db.programs.Rate.proposal_pk,
    ).where(
        db.programs.Proposal.slug == slug,
    ).group_by(
        db.programs.Proposal.pk,
    ).order_by(
        db.programs.Proposal.pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid proposal', 400

        return flask.jsonify({
            'Title'      : row.title,
            'Avg Rating' : row._mapping['avg(rating)'],
            'Relevance'  : row.Relevance,
            'Clarity'    : row.Clarity,
            'Engagement' : row.Engagement,
            'Content'    : row.Content,
            'Rated by'   : row._mapping['Rated by'],
            'Status'     : row.status,
        })


@app.post('/proposals/evaluation/<int:pk>')
def proposal_evaluation(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    status = flask.request.json.get('status', 'submitted')

    query = sa.update(
        db.programs.Proposal,
    ).where(
        db.programs.Proposal.pk == pk,
    ).values(
        status    = status,
        updatedBy = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return 'Proposal accepted', 202
