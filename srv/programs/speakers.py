import flask
import sqlalchemy as sa

import db
import db.events
import db.programs

from srv import app


@app.route('/programs/speakers')
def programs_speaker_list_page():
    query = sa.select(
        db.events.Attendee.pk,
        db.events.Attendee.name,
        db.events.Attendee.bio,
        db.events.Attendee.affiliation,

        db.programs.Proposal.title,
        db.programs.Proposal.abstract,
    ).where(
        db.programs.Proposal.session == 'keynote',
    ).outerjoin(
        db.programs.Proposal,
        db.programs.Proposal.attendee_pk == db.events.Attendee.pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        '/programs/speakers.djhtml',
        pageTitle = 'Speakers',
        pageDesc  = 'List of all submitted speakers',
        baseURL   = '/speakers',
        cursor    = cursor,
    )
