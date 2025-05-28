import io

import flask
import sqlalchemy as sa

import db
import db.conf
import db.programs

from srv import app


FILE_MAGIC_NUMBERS = {
    b'\xFF\xD8\xFF'      : ('image/jpeg', 'jpg'),
    b'\x89PNG\r\n\x1a\n' : ('image/png', 'png'),
}


@app.route('/programs/speakers')
def programs_speaker_list_page():
    query = sa.select(
        db.conf.Attendee.pk,
        db.conf.Attendee.name,
        db.conf.Attendee.bio,
        db.conf.Attendee.affiliation,

        db.programs.Proposal.pk.label('proposal_pk'),
        db.programs.Proposal.title,
        db.programs.Proposal.abstract,
        db.programs.Proposal.session,
        db.programs.Proposal.co_authors,
        db.programs.Proposal.slideBlob,
    ).where(
        db.programs.Proposal.status == 'accepted',
    ).outerjoin(
        db.programs.Proposal,
        db.programs.Proposal.attendee_pk == db.conf.Attendee.pk,
    ).order_by(
        db.conf.Attendee.name,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        speakers = [dict(row) for row in cursor.mappings()]

    return flask.render_template(
        '/programs/speakers.djhtml',
        pageTitle = 'Speakers',
        pageDesc  = 'List of all submitted speakers',
        baseURL   = '/speakers',
        speakers  = speakers,
    )


@app.route('/programs/speakers/<name>')
def programs_speaker_photoBlob(name):
    query = sa.select(
        db.conf.Attendee.photoBlob,
    ).where(
        db.conf.Attendee.name == name,
    )

    with db.engine.connect() as connection:
        blob = connection.execute(query).scalar()

        if blob is None:
            return flask.send_file (
                'static/speaker-avatar.png',
                mimetype = 'image/png',
            )
            return 'File Not Found', 404

        mimetype, ext = 'application/octet-stream', ''
        for magic, mime in FILE_MAGIC_NUMBERS.items():
            if not blob.startswith(magic): continue
            mimetype, ext = mime

        slug = name.lower().replace(' ', '-')
        return flask.send_file(
            io.BytesIO(blob),
            download_name = '{}.{}'.format(slug, ext),
            mimetype      = mimetype,
        )
