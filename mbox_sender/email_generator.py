#!/usr/bin/python3

import os
import sys
import psycopg2
import psycopg2.extras
from types import SimpleNamespace
from email_config import DB_CONFIG
import templates

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from srv.mbox.queue import add


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
                    WHERE "type" = 'participant'
                '''
            )
            for attendee in cursor.fetchall():
                att = SimpleNamespace(dict(attendee))
                add(attendee)
                print('Added: ', str(attendee))
    except Exception as e:
        print('ERROR : {}'.format(str(e)))
    finally:
        print("====== DONE ========")
