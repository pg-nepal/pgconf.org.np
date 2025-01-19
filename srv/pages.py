import flask
import jinja2
import uuid

from srv import app


@app.before_request
def assign_session_id():
    if 'session_id' not in flask.session:
        flask.session['session_id'] = str(uuid.uuid4())


@app.route('/')
def render_home():
    return flask.render_template(
        '/home.djhtml',
    )


@app.route('/<page>')
def render_page(page):
    try:
        return flask.render_template(
            page + '.djhtml'
        )
    except jinja2.exceptions.TemplateNotFound:
        return flask.render_template(
            '/pages/{}.djhtml'.format(page),
        )
    finally:
        flask.abort(404)


#@app.route('/pages/<page>')
def render_form_pages(page):
    try:
        return flask.render_template(
            '/pages/{}.djhtml'.format(page),
        )
    except jinja2.exceptions.TemplateNotFound:
        flask.abort(404)

@app.route('/about')
def render_about():
    return flask.render_template(
        'pages/about.djhtml',
    )

@app.route('/call_for_proposal')
def call_for_proposal():
    return flask.render_template(
        'pages/call_for_proposal.djhtml',
    )

@app.route('/register')
def registration():
    return flask.render_template(
        'pages/registration.djhtml',
    )

@app.route('/schedule')
def schedule():
    return flask.render_template(
        'pages/schedule.djhtml',
    )

@app.route('/venue')
def venue():
    return flask.render_template(
        'pages/venue.djhtml',
    )

@app.route('/code_of_conduct')
def code_of_conduct():
    return flask.render_template(
        'pages/code_of_conduct.djhtml',
    )