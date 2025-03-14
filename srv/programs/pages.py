import flask
import sqlalchemy as sa

import db
import db.conf
import db.programs

from srv import app


@app.route('/programs/training')
def programs_training_page():
    query = sa.select(
        db.conf.Attendee.pk,
        db.conf.Attendee.name,
        db.conf.Attendee.bio,
        db.conf.Attendee.affiliation,
    ).where(
        db.conf.Attendee.pk.in_([54, 55, 56]),
    ).order_by(
        db.conf.Attendee.pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        '/programs/training.djhtml',
        cursor = cursor,
    )
