from datetime import datetime, timedelta
import sqlalchemy as sa

import db
import db.mbox
import mbox_sender.templates

def add(attendee):
    # deadline is next day
    deadline = (datetime.today() + timedelta(days=1)).strftime('%d %B, %Y')
    subject   = 'PostgreSQL Conference Nepal - Registration (Next Step)'
    emailBody = mbox_sender.templates.registration (
        attendee.slug,
        attendee.type,
        attendee.name,
        attendee.email,
        'pending',
        attendee.category,
        deadline
    )

    query = sa.insert (
        db.mbox.MBox,
    ).values (
        type      = 'email',
        ref       = attendee.slug,
        to        = attendee.email,
        bcc       = 'info.pgconf@gmail.com',
        subject   = subject,
        body      = emailBody,
        createdBy = 'background',
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return True, {
            'message' : 'Email Queued for scheduled sending',
        }


def create_queue(ref, to, subject, body):
    query = sa.insert (
        db.mbox.MBox,
    ).values (
        type      = 'email',
        ref       = ref,
        to        = to,
        bcc       = 'info.pgconf@gmail.com',
        subject   = subject,
        body      = body,
        createdBy = 'background',
    )

    with db.SessionMaker.begin() as session:
        session.execute(query)
        return True, {
            'message' : 'Email Queued for scheduled sending',
        }
