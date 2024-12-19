#!venv/bin/python

import datetime as dt

import srv.pages
import srv.proposals

from srv import app


app.jinja_env.globals.update({
    'eventOn' : dt.datetime(2025, 5, 5),
    'eventTo' : dt.datetime(2025, 5, 6),
})


if __name__ == '__main__':
    app.run(
        host  = '0.0.0.0',
        port  = 5000,
        debug = True,
    )
