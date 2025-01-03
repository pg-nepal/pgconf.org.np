import flask
import jinja2

from srv import app


@app.route('/')
def render_home():
    return flask.render_template(
        '/pages/home.djhtml',
    )


@app.route('/<page>')
def render_page(page):
    try:
        return flask.render_template(
            page + '.djhtml'
        )
    except jinja2.exceptions.TemplateNotFound:
        flask.abort(404)
