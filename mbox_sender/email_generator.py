#!/usr/bin/python3

import os
import sys
import json
import psycopg2
import psycopg2.extras

from email_config import DB_CONFIG
import templates

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from srv.mbox.queue import create_queue


def gen_from_db():
    try:
        with psycopg2.connect(**DB_CONFIG) as connection:
            cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            print('Reading registrations')

            sql = 'SELECT pk, slug, "type", "name", "email", status, category '
            sql = sql + 'FROM conf25.attendees '
            # sql = sql + '''WHERE "type" = 'speaker' '''
            sql = sql + '''WHERE "type" = 'participant' and "status" = 'pending' '''
            # select attendee_pk, status, "paymentStatus", currency   from conf25.tickets where currency ='NRs.' and  status not in ('paid','confirmed') and event_pk =2 ;
            sql = sql + ''' and pk in (select attendee_pk from conf25.tickets where currency ='NRs.' and  status not in ('paid','confirmed') and event_pk =2 )'''
            # print(sql)
            # return
            cursor.execute (sql)


            subject   = templates.PAYMENT_FOLLOWUP_SUB
            for attendee in cursor.fetchall():
                body = templates.PAYMENT_FOLLOWUP.format(
                    slug = attendee['slug'],
                    category = attendee['category'],
                    name = attendee['name'],
                    status = attendee['status'],
                    email = attendee['email'],
                )

                create_queue(
                    attendee['slug'],
                    attendee['email'],
                    subject,
                    body,
                )
                print('Added: ', str(attendee['email']))
    except Exception as e:
        print('ERROR : {}'.format(str(e)))
    finally:
        print("====== DONE ========")


def gen_from_json(contacts):
    for contact in contacts:
        body = templates.INTL_FINAL_CALL.format(
            slug = contact['slug'],
            name = contact['name'],
        )
        subject = templates.INTL_FINAL_CALL_SUB
        create_queue(
            contact['slug'],
            contact['email'],
            subject,
            body
        )
        print('Added: ', str(contact['email']))


if __name__ == '__main__':
    print('=== Email generation START ===')
    gen_from_db()
    # with open('mbox_sender/intl_followup.json') as fp:
    #     contacts = json.load(fp)
    #     gen_from_json(contacts)
    print('=== Email generation DONE  ===')
