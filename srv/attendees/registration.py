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


def generate_ticket(isMainConference, isTraining, category, limit):
    confFee     = 7000
    trainingFee = 10000
    tickets = []

    if isMainConference:
        discount_student = 2000 if category == 'student' else 0
        discount_early = 2000 if limit < 20 else 0
        confFee = confFee - discount_student - discount_early

        tickets.append({
            'ticketType'    : 'Main Conference',
            'fee'           : confFee,
            'paymentStatus' : 'unpaid',
        })

    totalFee = confFee
    if isTraining:
        totalFee = totalFee + trainingFee
        tickets.append({
            'ticketType'    : 'Pre-Conference Training',
            'fee'           : trainingFee,
            'paymentStatus' : 'unpaid',
        })

    return totalFee, tickets


@app.get('/registered/form')
def registered_form():
    idx = random.randrange(len(srv.captcha.questions))  # noqa:S311
    return flask.render_template(
        '/attendees/form-registration.djhtml',
        idx      = idx,
        question = srv.captcha.questions[idx][0],
    )


@app.post('/registered/add')
def registered_create():
    formData = flask.request.form.to_dict()

    idx = int(formData.pop('idx'))
    answer = formData.pop('answer').upper()

    if answer != srv.captcha.questions[idx][1]:
        return 'Incorrect answer', 400

    category = formData.get('category')
    with db.engine.connect() as connection:
        cursor = connection.execute(sa.select(
            sa.func.count().label('count'),
        ).where(
            db.conf.Attendee.category == category,
        ))

        limit_count = cursor.scalar()

    isMainConference = formData.get('isMainConference')
    if isMainConference: formData.pop('isMainConference')
    isTraining = formData.get('isTraining')
    if isTraining: formData.pop('isTraining')

    totalFee, tickets = generate_ticket(isMainConference, isTraining, category, limit_count)

    status = 'pending'
    ticket = 'ticket'

    query = sa.insert(
        db.conf.Attendee,
    ).values(
        **formData,
        isMainConference = True if isMainConference else False,
        isTraining       = True if isTraining else False,
        fee    = totalFee,
        status = status,
        ticket = ticket,
    ).returning(
        db.conf.Attendee.pk,
        db.conf.Attendee.slug,
    )

    try:
        with db.SessionMaker.begin() as session:
            cursor = session.execute(query)

            attendees = cursor.mappings().fetchall()
            slug = attendees[0]['slug']
            attendees_pk = attendees[0]['pk']

            # insert into the tickets
            tickets = [{**ticket, 'paidAmt' : 0, 'attendees_pk': attendees_pk} for ticket in tickets]

            query_ticket = sa.insert (
                db.conf.Ticket,
            ).values (
                tickets,
            ).returning (
                db.conf.Ticket.ticketType,
                db.conf.Ticket.fee,
            )
            cursor = session.execute(query_ticket)

            tickets = [list(row) for row in cursor]

            emailBody = flask.render_template(
                'emails/registration_thanks.djhtml',
                name     = formData['name'],
                email    = formData['email'],
                fee      = totalFee,
                category = category,
                status   = status,
                tickets  = [list(row) for row in cursor],
                slug     = slug,
            )
            subject = 'Thank You for registering for the PostgreSQL Conference - Next Steps'
            to      = formData['email']
            srv.mbox.out.queue(slug, to, None, subject, emailBody)
            # not returning 201 because of redirection
            return flask.redirect('/registered/{}'.format(slug))
    except sa.exc.IntegrityError as e:
        if isinstance(e.orig, psycopg.errors.UniqueViolation):
            return 'email in used has already been registered', 400
        traceback.print_exc()
        raise e


@app.get('/registered/<slug>')
def registered_read(slug):
    query = sa.select(
        db.conf.Attendee.name,
        db.conf.Attendee.email,
        db.conf.Attendee.country,
        db.conf.Attendee.fee,
        db.conf.Attendee.slug,
        db.conf.Attendee.receiptPath,
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

    query = sa.update(
        db.conf.Attendee,
    ).where(
        sa.cast(db.conf.Attendee.slug, sa.String) == slug,
    ).values(
        receiptBlob = receiptBlob,
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400


@app.get('/registered/payment_receipt_check/<slug>')
def registered_payment_receipt_file_check(slug):
    query = sa.select(
        db.conf.Attendee.pk,
    ).where(
        sa.cast(db.conf.Attendee.slug, sa.String) == slug,
        db.conf.Attendee.receiptBlob.isnot(None),
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
        db.conf.Attendee.receiptBlob,
    ).where(
        sa.cast(db.conf.Attendee.slug, sa.String) == slug,
        db.conf.Attendee.receiptBlob.isnot(None),
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
