import flask

from srv import app


@app.route('/pages/speakers/all')
def render_speaker_page():
    from talks import keynotes,talks, workshops
    return flask.render_template(
        'speakers.djhtml',
        keynotes  = keynotes,
        talks     = talks,
        workshops = workshops,
    )


@app.route('/speaker/<slug>')
def render_speaker_page_slug(slug):
    from talks import keynotes,talks, workshops

    talks_list = keynotes + talks + workshops
    selected_talk = None

    for talk in talks_list:
        if talk['slug'] != slug:
            continue
        selected_talk = talk

    return flask.render_template(
        'speakers_indivisual.djhtml',
        talk = selected_talk,
    )
