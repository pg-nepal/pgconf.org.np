import base64
import io
import random
import traceback
import datetime as dt

import flask
import psycopg.errors
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql

import db
import db.conf

from srv import app

@app.get('/tickets/<slug>')
def ticket_read(slug):
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

        return flask.render_template(
            '/parts/ticket.djhtml',
            events = [row._asdict() for row in cursor],
        )
