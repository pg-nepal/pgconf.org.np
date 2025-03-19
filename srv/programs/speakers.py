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

        db.programs.Proposal.title,
        db.programs.Proposal.abstract,
    ).where(
        db.programs.Proposal.session == 'keynote',
    ).outerjoin(
        db.programs.Proposal,
        db.programs.Proposal.attendee_pk == db.conf.Attendee.pk,
    ).order_by(
        db.conf.Attendee.name,
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


@app.route('/programs/speakers/<name>')
def programs_speaker_photoBlob(name):
    query = sa.select(
        db.conf.Attendee.photoBlob,
    ).where(
        db.conf.Attendee.name == name,
        db.conf.Attendee.type == db.conf.e_attendees_type.speaker,
    )

    with db.engine.connect() as connection:
        blob = connection.execute(query).scalar()

        if blob is None:
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
