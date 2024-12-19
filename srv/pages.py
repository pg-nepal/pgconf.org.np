import flask

from srv import app


@app.route('/')
def render_home():
    return flask.render_template(
        '/pages/home.djhtml',
    )


@app.route('/<page>')
def render_page(page):
    return flask.render_template(
        page + '.djhtml'
    )
