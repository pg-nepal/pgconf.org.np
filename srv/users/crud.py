import flask

from srv import app


@app.get('/login')
def login_form():
    return flask.render_template('/')


@app.post('/login')
def login():
    return flask.render_template('/')

@app.get('/users')
def users_list():
    return flask.render_template('/')


@app.get('/users/<int:pk>')
def users_read(pk):
    return flask.render_template('/')

@app.delete('/users/<int:pk>')
def user_delete(pk):
    return flask.render_template('/')