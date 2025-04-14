#!/usr/bin/python3

import os
import sys
import psycopg2
from email_config import DB_CONFIG
import templates

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from srv.mbox.queue import add


if __name__ == '__main__':
    print('==Email generation ===')
    try:
        with psycopg2.connect(**DB_CONFIG) as connection:
            cursor = connection.cursor()
            print('Reading registrations')
            cursor.execute (
                '''
                    SELECT pk, slug, "type", "name", "email", status, category
                    FROM conf25.attendees
                    WHERE  email = 'rughimire@gmail.com'
                '''
                # WHERE -- "type" = 'participant' and
            )
            for attendee in cursor.fetchall():
                pk, slug, _type, name, email, status, category = attendee


                emailBody = templates.registration(slug, _type, name, email, status, category)
                subject = 'PostgreSQL Conference - Registration (Next Steps)'
                to      = email
                add(slug, to, None, subject, emailBody,)
                print(pk, slug, _type, name, email, status)
    except Exception as e:
        print('ERROR : {}'.format(str(e)))
    finally:
        print("====== DONE ========")
