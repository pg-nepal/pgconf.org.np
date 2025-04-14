import sqlalchemy as sa

import db
import db.mbox
import psycopg2

from mbox_sender.email_config import DB_CONFIG
from mbox_sender.templates import registration


def add(ref, to, cc, subject, body, type='email', note=None):
    query = sa.insert (
        db.mbox.MBox,
    ).values(
        type      = type,
        ref       = ref,
        to        = to,
        cc        = cc if cc != '' else None,
        subject   = subject,
        body      = body,
        note      = note,
        createdBy = 'background',
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return True, {
            'message' : 'Email Queued for scheduled sending',
        }


def generate_emails():
    print('==Email generation ===')
    try:
        with psycopg2.connect(**DB_CONFIG) as connection:
            cursor = connection.cursor()
            print('Reading registrations')
            cursor.execute (
                '''
                    SELECT pk, slug, "type", "name", "email", status, category
                    FROM conf25.attendees where "email" = 'rughimire@gmail.com'
                '''
                    # WHERE "type" = 'participant'

            )
            for attendee in cursor.fetchall():
                pk, slug, _type, name, email, status, category = attendee
                emailBody = registration(slug, _type, name, email, status, category)
                subject   = 'PostgreSQL Conference - registration'
                to        = email

                add(slug, to, None, subject, emailBody)

                print("Email generated ", pk, slug, _type, name, email, status)
    except Exception as e:
        print('ERROR : {}'.format(str(e)))
    finally:
        print("====== DONE ========")
