#!/usr/bin/python3

import os
import sys
import psycopg2
import psycopg2.extras
from email_config import DB_CONFIG
import templates

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from srv.mbox.queue import create_queue


if __name__ == '__main__':
    print('==Email generation ===')
    try:
        with psycopg2.connect(**DB_CONFIG) as connection:
            cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            print('Reading registrations')
            cursor.execute (
                '''
                    SELECT pk, slug, "type", "name", "email", status, category
                    FROM conf25.attendees
                    WHERE "type" = 'participant' and "status" = 'pending'
                '''
            )
            subject   = 'PostgreSQL Conference Nepal - Complete Registration'

            for attendee in cursor.fetchall():
                body = templates.PARTICIPANTS_PAYMENT_FOLLOWUP.format(
                    slug = attendee['slug'],
                    category = attendee['category'],
                    name = attendee['name'],
                    status = attendee['status'],
                    email = attendee['email'],
                )
                create_queue(attendee['slug'], attendee['email'], subject, body)
                print('Added: ', str(attendee['email']))
    except Exception as e:
        print('ERROR : {}'.format(str(e)))
    finally:
        print("====== DONE ========")
