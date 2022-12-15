#!venv/bin/python

import flask

app = flask.Flask(__name__)


@app.route('/')
def render_home():
    return flask.render_template(
        'home.html'
    )


@app.route('/<page>')
def render_page(page):
    return flask.render_template(
        page + '.html'
    )


if __name__ == '__main__':
    app.run(debug=True)
