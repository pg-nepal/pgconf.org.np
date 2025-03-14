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
import srv.captcha
import srv.mbox.out


from srv import app


FILE_MAGIC_NUMBERS = {
    b'%PDF-'                : 'application/pdf',
    b'\xFF\xD8\xFF'         : 'image/jpeg',
    b'\x89PNG\r\n\x1a\n'    : 'image/png',
}

def getTicketDetails(attendee, events):
    ticketList = []
    with db.engine.connect() as connection:
        cursor = connection.execute(sa.select(
            db.conf.Event.pk,
            db.conf.Event.feeGlobal,
            db.conf.Event.feeLocal,
            db.conf.Event.studentGlobal,
            db.conf.Event.studentLocal,
            db.conf.Event.earlyGlobal,
            db.conf.Event.earlyLocal,
            db.conf.Event.earlyLimit,
        ).where(
            db.conf.Event.pk.in_(list(map(int, events))),
        ))

        for row in cursor:
            cursor_count = connection.execute(sa.select(
                sa.func.count(),
            ).where(
                db.conf.Ticket.event_pk == row.pk,
            ))

            count = cursor_count.scalar()
            discount = 0

            if attendee.country.lower() == 'nepal':
                currency = 'NRs.'
                discount += row.studentLocal if attendee.category == 'student' else 0
                discount += row.earlyLocal if count <= row.earlyLimit else 0
                fee = row.feeLocal - discount

            else:
                currency = 'USD'
                discount += row.studentGlobal if attendee.category == 'student' else 0
                discount += row.earlyGlobal if count <= row.earlyLimit else 0
                fee = row.feeGlobal - discount

            ticketList.append({
                'attendee_pk'   : attendee.pk,
                'attendee_slug' : attendee.slug,
                'event_pk'      : row.pk,
                'currency'      : currency,
                'fee'           : fee,
            })

    return ticketList


@app.get('/registered/form')
def registered_form():
    idx = random.randrange(len(srv.captcha.questions))  # noqa:S311

    query = sa.select(
        db.conf.Event.pk,
        db.conf.Event.name,
        db.conf.Event.eventOn,
        db.conf.Event.eventTo,
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
                db.conf.Attendee,
            ).values(
                **jsonData,
            ).returning(
                db.conf.Attendee.pk,
                db.conf.Attendee.slug,
                db.conf.Attendee.email,
                db.conf.Attendee.country,
                db.conf.Attendee.category,
            ))

            attendee = cursor.first()

            cursor = session.execute(sa.insert(
                db.conf.Ticket,
            ).values(
                getTicketDetails(attendee, events),
            ))

            # srv.mbox.queue.after_registration(attendee)
            # not returning 201 because of redirection
        return flask.redirect('/registered/{}'.format(attendee.slug))
    except sa.exc.IntegrityError as e:
        if isinstance(e.orig, psycopg.errors.UniqueViolation):
            if e.orig.diag.constraint_name == 'attendees_email_key':
                return 'email in used has already been registered', 400
        traceback.print_exc()
        raise e


@app.get('/registered/<slug>')
def registered_read(slug):
    query = sa.select(
        db.conf.Attendee.pk,
        db.conf.Attendee.name,
        db.conf.Attendee.email,
        db.conf.Attendee.country,
        db.conf.Attendee.slug,
        db.conf.Attendee.category,
        db.conf.Attendee.idProofBlob,
        sa.cast(db.conf.Attendee.status, sa.String).label('status'),
    ).where(
        sa.cast(db.conf.Attendee.slug, sa.String) == slug,
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
                'Name'        : row.name,
                'Country'     : row.country,
                'Status'      : row.status,
                'Category'    : row.category,
                'idProofBlob' : row.idProofBlob,
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
        db.conf.Attendee.pk,
    ).where(
        sa.cast(db.conf.Attendee.slug, sa.String) == slug,
    ).scalar_subquery()

    query = sa.update(
        db.conf.Ticket,
    ).where(
        db.conf.Ticket.attendee_pk == subquery,
    ).values(
        receiptBlob = receiptBlob,
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400


@app.get('/registered/payment_receipt_check/<slug>')
def registered_payment_receipt_file_check(slug):
    query = sa.select(
        db.conf.Ticket.pk,
    ).join(
        db.conf.Attendee,
        db.conf.Ticket.attendee_pk == db.conf.Attendee.pk,
    ).where(
        sa.cast(db.conf.Attendee.slug, sa.String) == slug,
        db.conf.Ticket.receiptBlob.isnot(None),
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
        db.conf.Ticket.receiptBlob,
    ).join(
        db.conf.Attendee,
        db.conf.Ticket.attendee_pk == db.conf.Attendee.pk,
    ).where(
        sa.cast(db.conf.Attendee.slug, sa.String) == slug,
        db.conf.Ticket.receiptBlob.isnot(None),
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
        db.conf.Event.pk,
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
            cursor = cursor,
        )


@app.get('/registered/receipt/<slug>')
def registered_receipt_read(slug):
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


@app.post('/registered/addevent')
def registered_add_event():
    jsonData = flask.request.json

    with db.SessionMaker.begin() as session:
        row_attendee = session.execute(sa.select(
            db.conf.Attendee.pk,
            db.conf.Attendee.slug,
            db.conf.Attendee.email,
            db.conf.Attendee.country,
            db.conf.Attendee.category,
        ).where(
            db.conf.Attendee.slug == jsonData['slug'],
        )).first()

        cursor = session.execute(sa.select(
            db.conf.Ticket.pk,
            db.conf.Ticket.event_pk,
            db.conf.Event.name,
        ).outerjoin(
            db.conf.Event,
            db.conf.Ticket.event_pk == db.conf.Event.pk,
        ).where(
            db.conf.Ticket.attendee_slug == jsonData['slug'],
        ))

        for row in cursor:
            if row.event_pk in jsonData['events']:
                jsonData['events'].pop(row.event_pk)
                continue

            session.execute(sa.delete(
                db.conf.Ticket,
            ).where(
                db.conf.Ticket.event_pk      == row.event_pk,
                db.conf.Ticket.attendee_slug == jsonData['slug'],
                db.conf.Ticket.paymentStatus != 'paid',
                db.conf.Ticket.paymentStatus != 'in review',
            ))

        session.execute(sa.dialects.postgresql.insert(
            db.conf.Ticket,
        ).values(
            getTicketDetails(row_attendee, jsonData['events']),
        ).on_conflict_do_nothing())

    return 'updated', 202


@app.post('/registered/receipt_upload/<slug>')
def receipt_upload(slug):
    receiptFile = flask.request.files['file']
    event_pk = flask.request.form.get('event_pk')

    if not receiptFile:
        return 'File not uploaded', 400

    mimetype = receiptFile.content_type
    if mimetype not in FILE_MAGIC_NUMBERS.values():
        return 'Invalid file format. Please upload jpeg, png or pdf file', 400

    receiptBlob = receiptFile.read()

    with db.SessionMaker.begin() as session:
        cursor = session.execute(sa.update(
            db.conf.Ticket,
        ).where(
            db.conf.Ticket.event_pk == int(event_pk),
            sa.cast(db.conf.Ticket.attendee_slug, sa.String) == slug,
        ).values(
            receiptBlob   = receiptBlob,
            receiptType   = mimetype,
            paymentStatus = 'in review',
        ))
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400


@app.post('/registered/receipt_view/<slug>')
def receipt_view(slug):
    event_pk = flask.request.json['event_pk']

    with db.SessionMaker.begin() as session:
        row = session.execute(sa.select(
            db.conf.Ticket.receiptBlob,
            db.conf.Ticket.receiptType,
        ).where(
            db.conf.Ticket.event_pk == int(event_pk),
            sa.cast(db.conf.Ticket.attendee_slug, sa.String) == slug,
        )).first()

        encoded_image = base64.b64encode(row.receiptBlob).decode('utf-8')

        return flask.jsonify({
            'image'       : encoded_image,
            'receiptType' : row.receiptType,
        })


@app.post('/registered/student_id_upload/<slug>')
def student_id_upload(slug):
    idFile = flask.request.files['file']

    if idFile is None:
        return 'File not uploaded', 400

    idProofType = idFile.content_type
    if idProofType not in FILE_MAGIC_NUMBERS.values():
        return 'Invalid file format. Please upload jpeg, png or pdf file', 400

    idProofBlob = idFile.read()

    try:
        with db.SessionMaker.begin() as session:
            cursor = session.execute(sa.update(
                db.conf.Attendee,
            ).where(
                sa.cast(db.conf.Attendee.slug, sa.String) == slug,
            ).values(
                idProofBlob = idProofBlob,
                idProofType = idProofType,
            ))
            return 'Updated Rows', 202 if cursor.rowcount > 0 else 400
    except Exception:
        traceback.print_exc()
        return 'Something went wrong. Try again later.', 400


@app.post('/registered/student_id_view/<slug>')
def student_id_view(slug):

    with db.SessionMaker.begin() as session:
        row = session.execute(sa.select(
            db.conf.Attendee.idProofBlob,
            db.conf.Attendee.idProofType,
        ).where(
            sa.cast(db.conf.Attendee.slug, sa.String) == slug,
        )).first()

        encoded_image = base64.b64encode(row.idProofBlob).decode('utf-8')

        return flask.jsonify({
            "image"         : encoded_image,
            "idProofType"   : row.idProofType,
        })
