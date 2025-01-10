import flask
import jinja2

from srv import app


@app.route('/')
def render_home():
    return flask.render_template(
        '/pages/home.djhtml',
    )


@app.route('/pages/<page>')
def render_form_pages(page):
    try:
        return flask.render_template(
            '/pages/{}.djhtml'.format(page),
        )
    except jinja2.exceptions.TemplateNotFound:
        flask.abort(404)
