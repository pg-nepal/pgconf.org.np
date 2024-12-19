#!venv/bin/python

import datetime as dt

import srv.pages
from srv import app


eventTo = dt.datetime(2025, 5, 6)
eventOn = dt.datetime(2025, 5, 5)

app.jinja_env.globals.update({
    'eventOn' : eventOn,
    'eventTo' : eventTo,
})


if __name__ == '__main__':
    app.run(
        host  = '0.0.0.0',
        port  = 5000,
        debug = True,
    )
