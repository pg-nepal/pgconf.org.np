import io
import flask
import sqlalchemy as sa

import db
import db.programs

from srv import app


@app.route('/proposals/<int:pk>.slide')
def proposal_read_slide(pk):
    query = sa.select(
        db.programs.Proposal.slideBlob,
        db.programs.Proposal.slideMime,
    ).where(
        db.programs.Proposal.pk == pk,
    )

    with db.engine.connect() as connection:
        row = connection.execute(query).first()

        if row is None:
            return 'File Not Found', 404

        return flask.send_file(
            io.BytesIO(row.slideBlob),
            mimetype      = row.slideMime,
            as_attachment = True,
            download_name = 'pgconf2025_slide.{}'.format(row.slideMime),
        )
