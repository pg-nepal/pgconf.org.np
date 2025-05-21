import io
import flask
import sqlalchemy as sa

import db
import db.programs

from srv import app


@app.route('/proposals/<int:pk>.slide')
def proposal_read_slide(pk):
    query = sa.select(
        db.programs.Proposal.name,
        db.programs.Proposal.title,
        db.programs.Proposal.slideBlob,
        db.programs.Proposal.slideMime,
    ).where(
        db.programs.Proposal.pk == pk,
    )

    with db.engine.connect() as connection:
        row = connection.execute(query).first()

        if row is None:
            return 'File Not Found', 404

        mime = row.slideMime
        return flask.send_file(
            io.BytesIO(row.slideBlob),
            mimetype      = mime,
            as_attachment = True,
            download_name = '{speaker} - {title}.{ext}'.format(
                speaker = row.name.encode('ascii', 'ignore').decode(),
                title   = ''.join(c for c in row.title if c.isalnum() or (c in '-_ ')),  # noqa:E501
                ext     = mime.partition('/')[-1],
            ),
        )
