import flask
import sqlalchemy as sa

import db
import db.users

from srv import app
from werkzeug.security import check_password_hash

@app.post('/signup')
def signup():
    formdata = flask.request.form.to_dict()

    username = formdata.get('username')
    email = formdata.get('email')
    password = formdata.get('password')

    with db.Session() as session:

        existing_user = session.query(db.users.Users).filter_by(username=username).first()
        existing_email = session.query(db.users.Users).filter_by(email=email).first()

        if existing_user or existing_email:
            flask.flash('Username already exists.', 'danger')
            return flask.redirect('/signup')

        new_user = db.users.Users(
            username=username,
            email=email
        )
        new_user.set_password(password)
        session.add(new_user)
        session.commit()

    flask.flash('signup successful. Please log in.', 'success')
    
    return flask.redirect('/login')

@app.get('/signup')
def signup_form():
    return flask.render_template('signupform.djhtml')

@app.post('/login')
def login():
    formdata = flask.request.form.to_dict()
    username = formdata.get('username')
    password = formdata.get('password')
    # Checking if the user exits and if the password is correct
    with db.Session() as session:
        user = session.query(db.users.Users).filter_by(username=username).first()

    if not user:
        flask.flash('Invalid username or password', 'danger')
        return flask.redirect('/login')

    if not user.check_password(password):
        flask.flash('Invalid username or password', 'danger')
        return flask.redirect('/login')

    flask.session['username'] = username
    flask.flash('Logged in.', 'success')
    return flask.redirect('/')


@app.get('/login')
def login_form():
    return flask.render_template('login.djhtml')

@app.get('/users')
def users_list():
    return flask.render_template('/')

@app.get('/users/<int:pk>')
def users_read(pk):
    return flask.render_template('/')

@app.delete('/users/<int:pk>')
def user_delete(pk):
    return flask.render_template('/')