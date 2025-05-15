import flask
import sqlalchemy as sa

import db
import db.conf

from srv import app


@app.get('/api/talks')
def talks_list():
    query = sa.select(
        db.programs.Proposal.slug,
        db.programs.Proposal.name,
        db.programs.Proposal.session,
        db.programs.Proposal.title,
    ).where(
        db.programs.Proposal.status == 'accepted',
    ).order_by(
        db.programs.Proposal.session,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        return flask.jsonify(
            [row._asdict() for row in cursor],
        )


@app.get('/talks/<slug>')
def talk_read(slug):
    query = sa.select(
        db.programs.Proposal.pk,
        db.programs.Proposal.name,
        db.programs.Proposal.session,
        db.programs.Proposal.title,
        db.programs.Proposal.abstract,
        db.programs.Proposal.attendee_pk,
        db.programs.Proposal.slideBlob,

        db.conf.Attendee.pk.label('attendee_pk'),
        db.conf.Attendee.bio,
        db.conf.Attendee.affiliation,
    ).outerjoin(
        db.conf.Attendee,
        db.programs.Proposal.attendee_pk == db.conf.Attendee.pk,
    ).where(
        db.programs.Proposal.slug == slug,
        db.programs.Proposal.status == 'accepted',
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        return flask.render_template(
            '/proposals/talk.djhtml',
            row = row,
        )
