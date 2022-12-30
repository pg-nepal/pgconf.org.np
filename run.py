#!venv/bin/python

import datetime as dt

import flask

eventOn = dt.datetime(2023, 5, 11)
eventTo = dt.datetime(2023, 5, 12)

app = flask.Flask(__name__)

app.jinja_env.globals.update({
    'eventOn' : eventOn,
    'eventTo' : eventTo,
})


@app.route('/')
def render_home():
    return flask.render_template(
        'home.djhtml',
    )


@app.route('/<page>')
def render_page(page):
    return flask.render_template(
        page + '.djhtml'
    )


if __name__ == '__main__':
    app.run(debug=True)
