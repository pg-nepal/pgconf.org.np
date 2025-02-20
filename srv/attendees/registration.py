import random
import io
import traceback

import flask
import psycopg.errors
import sqlalchemy as sa

import db
import db.events
import srv.captcha
import uploads

from srv import app


FILE_MAGIC_NUMBERS = {
    b'%PDF-'                : 'application/pdf',
    b'\xFF\xD8\xFF'         : 'image/jpeg',
    b'\x89PNG\r\n\x1a\n'    : 'image/png',
}


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
            db.events.Attendee.category == category,
        ))

        count = cursor.scalar()

    discount_student = 2000 if category == 'student' else 0
    discount_early = 2000 if count < 20 else 0

    query = sa.insert(
        db.events.Attendee,
    ).values(
        **formData,
        fee    = 7000 - discount_student - discount_early,
        status = 'pending',
        ticket = 'ticket',
    ).returning(
        db.events.Attendee.slug,
    )

    try:
        with db.SessionMaker.begin() as session:
            cursor = session.execute(query)
            # not returning 201 because of redirection
            return flask.redirect('/registered/{}'.format(cursor.scalar()))
    except sa.exc.IntegrityError as e:
        if not isinstance(e, psycopg.errors.UniqueViolation):
            return 'email in used has already been registered', 400
        traceback.print_exc()


@app.get('/registered/<slug>')
def registered_read(slug):
    query = sa.select(
        db.events.Attendee.name,
        db.events.Attendee.email,
        db.events.Attendee.country,
        db.events.Attendee.fee,
        db.events.Attendee.slug,
        db.events.Attendee.receiptPath,
        sa.cast(db.events.Attendee.status, sa.String).label('status'),
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
    
    query = sa.update(
        db.events.Attendee,
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
    ).values(
        paymentReceiptFile = receiptBlob,
    )
    try:
        with db.SessionMaker.begin() as session:
            cursor = session.execute(query)
            return 'Updated Rows', 202 if cursor.rowcount > 0 else 400
    except Exception as e:
        traceback.print_exc()
        return 'Something went wrong while saving file. Try again later.', 400


@app.get('/registered/payment_receipt_check/<slug>')
def registered_payment_receipt_file_check(slug):
    query = sa.select(
        db.events.Attendee.pk
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
        db.events.Attendee.paymentReceiptFile.isnot(None),
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
        db.events.Attendee.paymentReceiptFile
    ).where(
        sa.cast(db.events.Attendee.slug, sa.String) == slug,
        db.events.Attendee.paymentReceiptFile.isnot(None),
    )

    with db.engine.connect() as connection:
        row = connection.execute(query).first()
        
        if row is None:
            return 'File Not Found', 404
        
        paymentReceiptFile = row[0]
        
        for magic, mime_type in FILE_MAGIC_NUMBERS.items():
            if paymentReceiptFile.startswith(magic): break
            else: mime_type = 'application/octet-stream'
        
        download_name = 'payment-receipt-{slug}.{ext}'.format(
            slug = slug,
            ext = mime_type.split('/')[1]
        )
        return flask.send_file(
            io.BytesIO(paymentReceiptFile),
            as_attachment       = True,
            download_name       = download_name,
            mimetype            = mime_type,
        ),200
