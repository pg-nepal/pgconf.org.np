import random

import flask
import sqlalchemy as sa

import db
import db.events
import srv.captcha
import uploads

from srv import app


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
            return flask.jsonify({
                'redirect': '/registered/{}'.format(cursor.scalar()),
            }), 201

    except Exception as e:
        return flask.jsonify({
            'error': 'Registration with the following email already exists',
        }), 400


@app.get('/registered/<slug>')
def registered_read_client(slug):
    query = sa.select(
        db.events.Attendee.name,
        db.events.Attendee.email,
        db.events.Attendee.country,
        db.events.Attendee.fee,
        db.events.Attendee.slug,
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
            row = row._asdict(),
        )


@app.post('/registered/<slug>')
def registered_update(slug):
    fileData = flask.request.files

    fullpath = uploads.save(fileData, 'receipt_url')

    query = sa.update(
        db.events.Attendee,
    ).where(
        db.events.Attendee.slug == slug.encode(),
    ).values(
        receipt_url = fullpath,
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400
