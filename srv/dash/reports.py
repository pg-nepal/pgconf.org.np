import flask
import sqlalchemy as sa

import srv.auth
import db

from srv import app


@app.get('/reports/registration_status')
@srv.auth.auth_required()
def reports_registration_status():
    sql = """

    """
    return flask.render_template(
        '/dash/reports/registration_status.djhtml',
        isAdmin = srv.auth.loggedInUser(flask.request),
    )


def get_registration_tickets_status():
    sql = """
        select e."name" event_name , t.status ticket_status, count(t.status) as total
        from conf25.tickets t
        inner join conf25.events e on t.event_pk = e.pk
        group by event_name, ticket_status
        order by event_name, ticket_status
    """
    with db.engine.connect() as conn:
        with conn.execute(sa.text(sql)) as cursor:
            result = [row._asdict() for row in cursor.fetchall()]
            return result


def get_registration_payment_status():
    sql = """
        select e."name" event_name , t."paymentStatus" payment_status , count(t.status) as total
        from conf25.tickets t
        inner join conf25.events e on t.event_pk = e.pk
        group by event_name, payment_status
        order by event_name, payment_status
    """
    with db.engine.connect() as conn:
        with conn.execute(sa.text(sql)) as cursor:
            result = [row._asdict() for row in cursor.fetchall()]
            return result
