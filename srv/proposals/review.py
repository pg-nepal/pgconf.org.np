import flask
import sqlalchemy as sa

import db
import db.proposals
import srv.auth
from srv import app


@app.get('/proposals/review')
def proposal_list_review():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = (
        sa.select(
            db.proposals.Proposal,
            sa.func.coalesce(
                sa.func.round(sa.func.avg(db.proposals.Review.rating), 0),
            ).label('avg(rating)'),
        )
        .outerjoin(
            db.proposals.Review,
            db.proposals.Proposal.pk == db.proposals.Review.proposal_pk,
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
        result = cursor.fetchall()
        print('Bing:', result)

    return flask.render_template(
        '/proposals/read.djhtml',
        cursor=result,
    )
