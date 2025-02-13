import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.auth
import srv.captcha
from srv import app


@app.get('/api/proposals')
def proposal_list_api():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = (
        sa.select(
            db.proposals.Proposal.pk,
            db.proposals.Proposal.title,
            sa.func.coalesce(
                sa.func.round(sa.func.avg(db.proposals.Rating.rating), 0),
            ).label('avg(rating)'),
            db.proposals.Proposal.category,
            db.proposals.Proposal.createdOn,
        )
        .outerjoin(
            db.proposals.Rating,
            db.proposals.Proposal.pk == db.proposals.Rating.proposal_pk,
        )
        .group_by(
            db.proposals.Proposal.pk,
        )
        .order_by(
            sa.desc('avg(rating)').nulls_last(),
        )
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        return flask.jsonify(
            headers=tuple(c['name'] for c in query.column_descriptions),
            data=[list(row) for row in cursor],
        )