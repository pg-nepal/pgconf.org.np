import io
import random
import traceback

import flask
import psycopg.errors
import sqlalchemy as sa

import db
import db.events
import srv.captcha
import srv.mbox.out


from srv import app


FILE_MAGIC_NUMBERS = {
    b'%PDF-'                : 'application/pdf',
    b'\xFF\xD8\xFF'         : 'image/jpeg',
    b'\x89PNG\r\n\x1a\n'    : 'image/png',
}


def ticket_cost_pre(attendee):
    if attendee.country.lower() == 'nepal':
        currency, fee, student = ('NRs.', 10_000, 0)
    else:
        currency, fee, student = ('USD', 200, 0)

    discount  = 0
    discount += student if attendee.category == 'student' else 0
    return currency, fee - discount


def ticket_cost_main(attendee, limit=20):
    if attendee.country.lower() == 'nepal':
        currency, fee, early, student = ('NRs.', 7_000, 2_000, 2_000)
    else:
        currency, fee, early, student = ('USD', 300, 100, 0)

    with db.engine.connect() as connection:
        # count tickets early discount
        cursor = connection.execute(sa.select(
            sa.func.count().label('count'),
        ).where(
            db.events.Attendee.category == attendee.category,
        ))
        count = cursor.scalar()

    discount  = 0
    discount += student if attendee.category == 'student' else 0
    discount += early if count < limit else 0
    return currency, fee - discount


def tickets_generate(attendee, events):
    func = {
        "1" : ticket_cost_pre,
        "2" : ticket_cost_main,
    }

    ticket_list = []
    for e in events:
        currency, fee = func[e](attendee)
        ticket_list.append({
            'attendee_pk' : attendee.pk,
            'event_pk'    : e,
            'currency'    : currency,
            'fee'         : fee,
        })

    return ticket_list


@app.get('/registered/form')
def registered_form():
    idx = random.randrange(len(srv.captcha.questions))  # noqa:S311

    query = sa.select(
        db.events.Event.pk,
        db.events.Event.type,
        db.events.Event.name,
        db.events.Event.eventOn,
        db.events.Event.eventTo,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        '/form-captcha.djhtml',
        pageTitle = '/ Registration',
        fields    = '/attendees/form-part.djhtml',
        script    = '/static/attendees/form.mjs',
        question  = srv.captcha.questions[idx][0],
        idx       = idx,
        cursor    = cursor,
    )


@app.post('/registered/add')
def registered_create():
    jsonData = flask.request.json

    idx = jsonData.pop('idx')
    answer = jsonData.pop('answer').upper()
    if answer != srv.captcha.questions[idx][1]:
        return 'Incorrect answer', 400

    events = jsonData.pop('events')

    try:
        with db.SessionMaker.begin() as session:
            cursor = session.execute(sa.insert(
                db.events.Attendee,
            ).values(
                **jsonData,
            ).returning(
                db.events.Attendee.pk,
                db.events.Attendee.slug,
                db.events.Attendee.email,
                db.events.Attendee.country,
                db.events.Attendee.category,
            ))

            attendee = cursor.first()

            cursor = session.execute(sa.insert(
                db.events.Ticket,
            ).values(
                tickets_generate(attendee, events),
            ).returning(
                db.events.Ticket.event_pk,
                db.events.Ticket.fee,
            ))

            # srv.mbox.queue.after_registration(attendee)
            # not returning 201 because of redirection
            return flask.redirect('/registered/{}'.format(attendee.slug))
    except sa.exc.IntegrityError as e:
        if isinstance(e.orig, psycopg.errors.UniqueViolation):
            if e.orig.diag.constraint_name == 'attendees_email_key':
                return 'email in used has already been registered', 400
        traceback.print_exc()


@app.get('/registered/<slug>')
def registered_read(slug):
    query = sa.select(
        db.events.Attendee.name,
        db.events.Attendee.email,
        db.events.Attendee.country,
        db.events.Attendee.slug,
        sa.cast(db.events.Attendee.status, sa.String).label('status'),

        # db.events.Tickets.fee,
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid uuid', 400

        return flask.render_template(
            '/attendees/profile.djhtml',
            row  = row,
            show = {
                'Name'    : row.name,
                'Country' : row.country,
                'Status'  : row.status,
            },
        )


@app.post('/registered/<slug>')
def registered_update(slug):
    receiptFile = flask.request.files['receiptFile']

    if not receiptFile:
        return 'File not uploaded', 400

    mimetype = receiptFile.content_type
    if mimetype not in FILE_MAGIC_NUMBERS.values():
        return 'Invalid file format. Please upload jpeg, png or pdf file', 400

    receiptBlob = flask.request.files['receiptFile'].read()

    subquery = sa.select(
        db.events.Attendee.pk,
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
    ).scalar_subquery()

    query = sa.update(
        db.events.Ticket,
    ).where(
        db.events.Ticket.attendee_pk == subquery,
    ).values(
        receiptBlob = receiptBlob,
    )

    try:
        with db.SessionMaker.begin() as session:
            cursor = session.execute(query)
            return 'Updated Rows', 202 if cursor.rowcount > 0 else 400
    except Exception:
        traceback.print_exc()
        return 'Something went wrong. Try again later.', 400


@app.get('/registered/payment_receipt_check/<slug>')
def registered_payment_receipt_file_check(slug):
    query = sa.select(
        db.events.Ticket.pk,
    ).join(
        db.events.Attendee,
        db.events.Ticket.attendee_pk == db.events.Attendee.pk
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
        db.events.Ticket.receiptBlob.isnot(None),
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()
        if row is None:
            return 'File Not Found', 404

        return 'File exists', 200


@app.get('/registered/payment_receipt_download/<slug>')
def registered_payment_receipt_file_download(slug):
    query = sa.select(
        db.events.Ticket.receiptBlob,
    ).join(
        db.events.Attendee,
        db.events.Ticket.attendee_pk == db.events.Attendee.pk,
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
        db.events.Ticket.receiptBlob.isnot(None),
    )

    with db.engine.connect() as connection:
        receiptBlob = connection.execute(query).scalar()

        if receiptBlob is None:
            return 'File Not Found', 404

        for magic, mime_type in FILE_MAGIC_NUMBERS.items():
            if receiptBlob.startswith(magic): break
            mime_type = 'application/octet-stream'

        download_name = 'payment-receipt-{slug}.{ext}'.format(
            slug = slug,
            ext  = mime_type.split('/')[1],
        )
        return flask.send_file(
            io.BytesIO(receiptBlob),
            as_attachment = True,
            download_name = download_name,
            mimetype      = mime_type,
        )


@app.get('/registered/ticket/<slug>')
def registered_ticket_read(slug):
    query = sa.select(
        db.events.Event.name.label('Event'),
        db.events.Ticket.currency.label('Currency'),
        db.events.Ticket.fee.label('Amount'),
        db.events.Ticket.paymentStatus.label('Payment Status'),
    ).join(
        db.events.Attendee,
        db.events.Ticket.attendee_pk == db.events.Attendee.pk,
    ).join(
        db.events.Event,
        db.events.Ticket.event_pk == db.events.Event.pk,
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        return flask.jsonify(
            headers = tuple(c['name'] for c in query.column_descriptions),
            data    = [list(row) for row in cursor],
        )
