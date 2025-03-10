import flask
import sqlalchemy as sa

import db
import db.conf

from srv import app


@app.get('/receipts/<slug>')
def receipt_read(slug):
    query = sa.select(
        db.conf.Event.pk.label('pk'),
        db.conf.Event.name.label('Event'),
        db.conf.Ticket.currency.label('Currency'),
        db.conf.Ticket.fee.label('Amount'),
        db.conf.Ticket.paymentStatus.label('Payment Status'),
    ).join(
        db.conf.Ticket,
        sa.and_(
            db.conf.Ticket.event_pk == db.conf.Event.pk,
            sa.cast(db.conf.Ticket.attendee_slug, sa.String) == slug,
        ),
    ).order_by(db.conf.Event.pk)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.render_template(
            '/parts/receipt.djhtml',
            cursor = cursor,
        )
