import traceback

import flask
import psycopg.errors
import sqlalchemy as sa

import db
import db.conf
import srv.auth

from srv import app


@app.get('/tickets')
def ticket_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/table.djhtml',
        pageTitle = 'tickets',
        pageDesc  = 'List of all registered tickets',
        baseURL   = '/tickets',
        isAdmin   = isAdmin,
    )


@app.post('/api/tickets')
def ticket_list_api():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    jsonData = flask.request.json

    query = sa.select(
        db.conf.Attendee.pk,
        db.conf.Attendee.name,
        db.conf.Attendee.category,
        sa.func.aggregate_strings(db.conf.Event.name, ", ").label('events'),
        sa.cast(db.conf.Ticket.status, sa.String).label('status'),
        db.conf.Ticket.currency,
        sa.func.aggregate_strings(sa.cast(sa.cast(db.conf.Ticket.fee, sa.Integer), sa.String), ' + ').label('fees'),
        sa.func.sum(db.conf.Ticket.fee).label('total'),
        sa.func.aggregate_strings(db.conf.Ticket.paymentStatus, ', ').label('payment_status'),
    ).join(
        db.conf.Ticket,
        db.conf.Ticket.attendee_pk == db.conf.Attendee.pk,
    ).join(
        db.conf.Event,
        db.conf.Event.pk == db.conf.Ticket.event_pk,
    ).group_by(
        db.conf.Attendee.pk,
        db.conf.Attendee.name,
        db.conf.Attendee.category,
        db.conf.Ticket.attendee_type,
        db.conf.Ticket.status,
        db.conf.Ticket.currency,
    )


    with db.engine.connect() as connection:
        cursor = connection.execute(query.where(*[
            c['expr'] == jsonData['filter'][c['name']]
            for c in query.column_descriptions
            if jsonData['filter'].get(c['name'], 'all') != 'all'
        ]).order_by(
            db.conf.Attendee.pk,
        ))

    return flask.jsonify(
        headers = (
            'pk', 'Name', 'Category', 'Registered for', 'Ticket Status',
            'Currency', 'Fees', 'Total', 'Payment Status'
        ),
        data    = [list(row) for row in cursor],
        filters = {

        },
    )
