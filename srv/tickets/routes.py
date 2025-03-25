import base64
import flask
import sqlalchemy as sa

import db
import db.conf

from srv import app
import srv


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
            db.conf.Ticket.status   != 'cancelled',
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
        db.conf.Event.pk,
        db.conf.Event.name.label('Event'),
        sa.func.concat(db.conf.Ticket.currency, ' ', db.conf.Ticket.fee).label('Amount'),
        sa.cast(db.conf.Ticket.status.label('Ticket Status'), sa.String),
        db.conf.Ticket.paymentStatus.label('Payment Status'),
        db.conf.Ticket.createdOn.label('Ordered Date'),
        db.conf.Ticket.receiptType.label('Receipt'),
        sa.literal('').label('Action'),
        sa.literal('').label('Change Status'),
    ).outerjoin(
        db.conf.Ticket,
        sa.and_(
            db.conf.Ticket.event_pk == db.conf.Event.pk,
            db.conf.Ticket.status   != 'cancelled',
            sa.cast(db.conf.Ticket.attendee_slug, sa.String) == slug,
        ),
    ).order_by(db.conf.Event.pk)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [row._asdict() for row in cursor],
        )


@app.get('/tickets/receipt/history/<int:pk>')
def receipt_history(pk):
    query = sa.select(
        db.conf.Receipt.pk,
        db.conf.Event.name.label('Event'),
        db.conf.Receipt.paymentStatus.label('Status'),
        db.conf.Receipt.paymentNote.label('Note'),
        db.conf.Receipt.updatedOn.label('Updated On'),
        sa.literal('').label('Receipt'),
    ).outerjoin(
        db.conf.Event,
        sa.and_(
            db.conf.Receipt.event_pk == db.conf.Event.pk,
        ),
    ).where(
        db.conf.Receipt.attendee_pk == pk,
    ).order_by(db.conf.Receipt.pk)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [row._asdict() for row in cursor],
        )


@app.get('/registered/tickets/receipt/<slug>')
def receipt_read_client(slug):
    query = sa.select(
        db.conf.Event.pk,
        db.conf.Event.name.label('Event'),
        sa.func.concat(db.conf.Ticket.currency, ' ', db.conf.Ticket.fee).label('Amount'),
        sa.cast(db.conf.Ticket.status.label('Ticket Status'), sa.String),
        db.conf.Ticket.paymentStatus.label('Payment Status'),
        db.conf.Ticket.createdOn.label('Ordered Date'),
        db.conf.Ticket.paymentNote.label('Note'),
        sa.literal('').label('Receipt'),
        sa.literal('').label('Action'),
    ).outerjoin(
        db.conf.Ticket,
        sa.and_(
            db.conf.Ticket.event_pk == db.conf.Event.pk,
            db.conf.Ticket.status   != 'cancelled',
            sa.cast(db.conf.Ticket.attendee_slug, sa.String) == slug,
        ),
    ).order_by(db.conf.Event.pk)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [row._asdict() for row in cursor],
        )


@app.post('/tickets/receipt/changestatus/<int:pk>')
def receipt_changestatus(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    event_name = flask.request.form.get('event_name')
    ticketStatus = flask.request.form.get('ticket-status')
    paymentStatus = flask.request.form.get('receipt-status')
    paymentNote = flask.request.form.get('note')

    with db.SessionMaker.begin() as session:
        row_event = session.execute(sa.select(
            db.conf.Event.pk,
        ).where(
            db.conf.Event.name == event_name,
        )).first()

        row = session.execute(sa.select(
            db.conf.Ticket.pk,
            db.conf.Ticket.receiptBlob,
            db.conf.Ticket.receiptType,
        ).where(
            db.conf.Ticket.event_pk == row_event.pk,
            db.conf.Ticket.attendee_pk == pk,
        )).first()

        cursor = session.execute(sa.update(
            db.conf.Ticket,
        ).where(
            db.conf.Ticket.event_pk == row_event.pk,
            db.conf.Ticket.attendee_pk == pk,
        ).values(
            status          = ticketStatus,
            paymentStatus   = paymentStatus,
            paymentNote     = paymentNote,
            updatedBy       = isAdmin,
        ))

        cursor_receipt = session.execute(sa.insert(
            db.conf.Receipt,
        ).values(
            ticket_pk     = row.pk,
            event_pk      = row_event.pk,
            attendee_pk   = pk,
            receiptBlob   = row.receiptBlob,
            receiptType   = row.receiptType,
            paymentStatus = paymentStatus,
            paymentNote   = paymentNote,
            createdBy     = isAdmin,
        ))
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400


@app.post('/ticket/receipt_view/<int:pk>')
def receipt_view_history(pk):
    with db.SessionMaker.begin() as session:
        row = session.execute(sa.select(
            db.conf.Receipt.receiptBlob,
            db.conf.Receipt.receiptType,
        ).where(
            db.conf.Receipt.pk == pk,
        )).first()

        encoded_image = base64.b64encode(row.receiptBlob).decode('utf-8')

        return flask.jsonify({
            'image'       : encoded_image,
            'receiptType' : row.receiptType,
        })
