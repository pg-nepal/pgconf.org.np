import io
import random
import traceback

import flask
import psycopg.errors
import sqlalchemy as sa

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


def ticket_cost_pre(category, fee=10_000):
    return fee


def ticket_cost_main(category, fee=7_000, limit=20):
    with db.engine.connect() as connection:
        # count tickets early discount
        cursor = connection.execute(sa.select(
            sa.func.count().label('count'),
        ).where(
            db.conf.Attendee.category == category,
        ))
        count = cursor.scalar()

    discount_student = 2_000 if category == 'student' else 0
    discount_early = 2_000 if count < limit else 0
    return fee - discount_student - discount_early


def tickets_generate(attendee, events):
    func = {
        db.conf.e_tickets_type.pre.name  : ticket_cost_pre,
        db.conf.e_tickets_type.main.name : ticket_cost_main,
    }

    ticket_list = []
    for e in events:
        ticket_list.append({
            'attendee_pk' : attendee.pk,
            'type'        : e,
            'fee'         : func[e](attendee.category),
        })

    return ticket_list


@app.get('/registered/form')
def registered_form():
    idx = random.randrange(len(srv.captcha.questions))  # noqa:S311
    return flask.render_template(
        '/form-captcha.djhtml',
        pageTitle = '/ Registration',
        fields    = '/attendees/form-part.djhtml',
        script    = '/static/attendees/form.mjs',
        question  = srv.captcha.questions[idx][0],
        idx       = idx,
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
                db.conf.Attendee.category,
            ))

            attendee = cursor.mappings().first()

            cursor = session.execute(sa.insert(
                db.conf.Ticket,
            ).values(
                tickets_generate(attendee, events),
            ).returning(
                db.conf.Ticket.type,
                db.conf.Ticket.fee,
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
        db.conf.Attendee.name,
        db.conf.Attendee.email,
        db.conf.Attendee.country,
        db.conf.Attendee.slug,
        sa.cast(db.conf.Attendee.status, sa.String).label('status'),

        # db.conf.Tickets.fee,
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
        db.conf.Ticket.attendee_pk == db.conf.Attendee.pk
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
        db.conf.Ticket.attendee_pk == db.conf.Attendee.pk
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
