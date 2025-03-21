import flask
import sqlalchemy as sa

import db
import db.conf

from srv import app


@app.get('/ticket/<slug>')
def ticket_show_mine(slug):
    query = sa.select(
        db.conf.Event.pk,
        db.conf.Event.name,
        db.conf.Event.eventOn,
        db.conf.Event.eventTo,
        db.conf.Ticket.status,
        db.conf.Ticket.currency,
        db.conf.Ticket.fee,
        db.conf.Ticket.paymentStatus,
        db.conf.Ticket.createdOn,
        db.conf.Ticket.updatedOn,
    ).outerjoin(
        db.conf.Ticket,
        sa.and_(
            db.conf.Ticket.event_pk == db.conf.Event.pk,
            db.conf.Ticket.status   == 'booked',
            sa.cast(db.conf.Ticket.attendee_slug, sa.String) == slug,
        ),
    ).order_by(db.conf.Event.pk)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.render_template(
            '/parts/ticket.djhtml',
            cursor = cursor,
        )


@app.get('/tickets/receipt/<slug>')
def receipt_read(slug):
    query = sa.select(
        db.conf.Event.pk.label('pk'),
        db.conf.Event.name.label('Event'),
        db.conf.Event.eventOn.label('Date From'),
        db.conf.Event.eventTo.label('Date To'),
        db.conf.Ticket.currency.label('Currency'),
        db.conf.Ticket.fee.label('Amount'),
        db.conf.Ticket.paymentStatus.label('Payment Status'),
        db.conf.Ticket.createdOn.label('Ordered Date'),
        db.conf.Ticket.updatedOn.label('Updated Date'),
    ).outerjoin(
        db.conf.Ticket,
        sa.and_(
            db.conf.Ticket.event_pk == db.conf.Event.pk,
            sa.cast(db.conf.Ticket.attendee_slug, sa.String) == slug,
        ),
    ).order_by(db.conf.Event.pk)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [list(row) for row in cursor],
        )
