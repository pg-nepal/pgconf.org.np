import flask

from srv import app


@app.route('/programs/speakers')
def programs_speaker_list_page():
    return flask.render_template(
        '/proposals/speakers.djhtml',
        # keynotes  = keynotes,
        # talks     = talks,
        # workshops = workshops
    )


@app.route('/programs/speakers/<slug>')
def programs_speaker_page(slug):
    return flask.render_template(
        'speakers_indivisual.djhtml',
        # talk = selected_talk,
    )
