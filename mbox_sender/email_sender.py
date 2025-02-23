#!/usr/bin/python3

import ssl
import email
import smtplib
import datetime as dt

import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import psycopg2

from mbox_sender.email_config import SMTP_CONFIG, DB_CONFIG


def compose(to, subject, body, cc =None, bcc=None):
    try:
        msg = MIMEMultipart()
        msg['Subject']  = subject
        msg['From']     = email.utils.formataddr(SMTP_CONFIG['SENDER'])
        msg['To']       = to

        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        return msg
    except Exception as ex:
        log("Compose ERROR: "+ str(ex))
        return None


def log(message):
    print('\033[35m{}\033[0m :: {}'.format( dt.datetime.now(), message ))


def connectSMTP():
    try:
        context = ssl.create_default_context()
        smtpConnection = smtplib.SMTP_SSL(SMTP_CONFIG['HOST'], 465, context=context)
        # smtpConnection.set_debuglevel(1)
        smtpConnection.login(SMTP_CONFIG['USER'], SMTP_CONFIG['PWD'])
        log('SMTP server connected')
        return smtpConnection
    except Exception as ex:
        log("ERROR {}".format(str(ex)))
        return None


if __name__ == '__main__':
    log('Email sending started')
    smtpConnection = connectSMTP()
    if not smtpConnection: exit(-1)

    try:
        with psycopg2.connect(**DB_CONFIG) as connection:
            cursor = connection.cursor()
            log('Reading emails')
            cursor.execute (
                '''
                    SELECT "pk", "to", "cc", "bcc", "subject", "body"
                    FROM conf25.mboxes
                    WHERE "isSent" = False
                '''
            )
            for mbox in cursor.fetchall():
                pk, to, cc, bcc, subject, body = mbox

                message = compose(to, subject, body, cc=cc, bcc=bcc)
                if not message: continue

                response = smtpConnection.send_message(msg=message)
                if not response:
                    cursor.execute (
                        '''
                            UPDATE conf25.mboxes
                            SET "isSent"=True
                            WHERE pk={}
                        '''.format(pk)
                    )
                    log('Queued email for PK={} => {}'.format(pk, to))
                else:
                    log('ERROR: Queue failed for PK={} => {}, {}'.format(pk, to, str(response)))
            cursor.close()
    except Exception as e:
        # Handle database-specific errors
        log('DB ERROR : {}'.format(str(e)))
        exit(-1)
    finally:
        smtpConnection.close()
        log('Email sending completed')
