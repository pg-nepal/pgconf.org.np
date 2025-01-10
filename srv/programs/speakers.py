import flask

from srv import app


@app.route('/programs/speakers')
def programs_speaker_list_page():
    return flask.render_template(
        '/programs/speakers.djhtml',
    )
