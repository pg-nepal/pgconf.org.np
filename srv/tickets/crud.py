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
        db.conf.Ticket.pk,
        db.conf.Ticket.event_pk,
        db.conf.Attendee.name,
        db.conf.Attendee.category,
        sa.cast(db.conf.Ticket.attendee_type, sa.String),
        db.conf.Ticket.currency,
        db.conf.Ticket.fee,
        db.conf.Ticket.createdOn,
        sa.cast(db.conf.Ticket.status, sa.String).label('status'),
    ).outerjoin(
        db.conf.Attendee,
        db.conf.Ticket.attendee_pk == db.conf.Attendee.pk,
    ).group_by(
        db.conf.Ticket.pk,
        db.conf.Attendee.name,
        db.conf.Attendee.category,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query.where(*[
            c['expr'] == jsonData['filter'][c['name']]
            for c in query.column_descriptions
            if jsonData['filter'].get(c['name'], 'all') != 'all'
        ]).order_by(
            db.conf.Ticket.pk,
        ))

    return flask.jsonify(
        headers = tuple(c['name'] for c in query.column_descriptions),
        data    = [list(row) for row in cursor],
        filters = {

        },
    )
