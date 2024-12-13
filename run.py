#!venv/bin/python

import datetime as dt
import flask
from server import create_tables

eventOn = dt.datetime(2025, 5, 5)
eventTo = dt.datetime(2025, 5, 6)

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


@app.route('/speakers/all')
def render_speaker_page():
    from talks import keynotes,talks, workshops
    return flask.render_template(
        'speakers.djhtml',
        keynotes  = keynotes,
        talks     = talks,
        workshops = workshops    
    )


@app.route('/speaker/<slug>')
def render_speaker_page_slug(slug):
    from talks import keynotes,talks, workshops

    talks_list = keynotes + talks + workshops
    selected_talk = None

    for talk in talks_list:
        if talk['slug'] != slug: continue
        selected_talk = talk
    print(selected_talk)
    return flask.render_template(
        'speakers_indivisual.djhtml', 
        talk     = selected_talk
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug = True)
