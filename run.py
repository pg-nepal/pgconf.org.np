#!venv/bin/python

import datetime as dt

import flask

eventOn = dt.datetime(2025, 5, 5)
eventTo = dt.datetime(2025, 5, 6)

app = flask.Flask(__name__)

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
