import traceback

import flask
import psycopg.errors
import sqlalchemy as sa

import db
import db.conf
import srv.auth

from srv import app


@app.get('/attendees/form')
def attendee_form():
    query = sa.select(
        db.conf.Event.pk,
        db.conf.Event.name,
        db.conf.Event.eventOn,
        db.conf.Event.eventTo,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        '/attendees/form.djhtml',
        cursor = cursor,
    )


@app.get('/attendees')
def attendee_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/table.djhtml',
        pageTitle = 'Attendees',
        pageDesc  = 'List of all registered attendees',
        baseURL   = '/attendees',
        isAdmin   = isAdmin,
    )


@app.post('/api/attendees')
def attendee_list_api():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    jsonData = flask.request.json

    query = sa.select(
        db.conf.Attendee.pk,
        db.conf.Attendee.name,
        db.conf.Attendee.country,
        db.conf.Attendee.category,
        sa.cast(db.conf.Attendee.type, sa.String).label('type'),
        db.conf.Attendee.createdOn,
        sa.cast(db.conf.Attendee.status, sa.String).label('status'),
        sa.func.count(db.conf.Ticket.receiptBlob).label('#'),
    ).outerjoin(
        db.conf.Ticket,
        db.conf.Attendee.pk == db.conf.Ticket.attendee_pk,
    ).group_by(
        db.conf.Attendee.pk,
        db.conf.Ticket.receiptBlob,
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
        headers = tuple(c['name'] for c in query.column_descriptions),
        data    = [list(row) for row in cursor],
        filters = {
            'category' : ('all', 'professional', 'student'),
            'type'     : ('all', *db.conf.attendees_type),
            'status'   : ('all', *db.conf.attendees_status),
        },
    )


@app.post('/api/attendees/add')
def attendee_create():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    formData = flask.request.form

    query = sa.insert(
        db.conf.Attendee,
    ).values(
        **formData,
        createdBy = isAdmin,
    )

    with db.SessionMaker.begin() as session:
        try:
            cursor = session.execute(query)
        except sa.exc.IntegrityError as e:
            if isinstance(e.orig, psycopg.errors.UniqueViolation):
                if e.orig.diag.constraint_name == 'attendees_email_key':
                    return 'email in used has already been registered', 400
                traceback.print_exc()
                raise e

        return flask.jsonify(
            pk = cursor.inserted_primary_key[0],
        )


@app.get('/attendees/<int:pk>')
@srv.auth.auth_required()
def attendee_read(pk):
    query = sa.select(
        db.conf.Attendee,
    ).where(
        db.conf.Attendee.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return 'Invalid pk', 400

        return flask.render_template(
            '/attendees/read.djhtml',
            isAdmin = srv.auth.loggedInUser(flask.request),
            row     = row,
            show    = {
                'Name'          : row.name,
                'Email'         : row.email,
                'Country'       : row.country,
                'Registered On' : row.createdOn.strftime('%B %d %Y'),
                'Category'      : row.category,
            },
        )


@app.post('/attendees/<slug>')
def attendee_update(slug):
    values = flask.request.form.to_dict()

    with db.SessionMaker.begin() as session:
        cursor = session.execute(sa.update(
            db.conf.Attendee,
        ).where(
            db.conf.Attendee.slug == slug,
        ).values(
            category = values.get('category'),
        ))
        return 'Updated Rows', 202 if cursor.rowcount > 0 else 400
