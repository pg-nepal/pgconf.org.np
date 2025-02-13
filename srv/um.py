import flask

import db
import db.users

from srv import app

from flask_jwt_extended import create_access_token


@app.post("/login")
def login():
    formdata = flask.request.form.to_dict()
    username = formdata.get("username")
    password = formdata.get("password")

    if not username or not password:
        flask.flash("Username and password are required.", "danger")
        return flask.redirect('/login')

    with db.Session() as session:
        user = session.query(db.users.Users).filter_by(username=username).first()  # noqa: E501

    # Checking if the user exists and if the password is correct
    if not user or not user.check_password(password):
        flask.flash("Invalid username or password", "danger")
        return flask.redirect("/login")

    access_token = create_access_token(identity=user.pk)
    flask.session["username"] = username
    return flask.jsonify({'message': 'Login Success', 'access_token': access_token}) # noqa: E501


@app.post("/signup")
def signup():
    formdata = flask.request.form.to_dict()

    username = formdata.get("username")
    email = formdata.get("email")
    password = formdata.get("password")

    with db.Session() as session:
        existing_user = (
            session.query(db.users.Users).filter_by(username=username).first()
        )
        existing_email = session.query(db.users.Users).filter_by(email=email).first() # noqa: E501

        if existing_user or existing_email:
            flask.flash("Username already exists.", "danger")
            return flask.redirect("/signup")

        new_user = db.users.Users(username=username, email=email)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()

    flask.flash("signup successful. Please log in.", "success")

    return flask.redirect("/login")


@app.get("/signup")
def signup_form():
    return flask.render_template("registration/signupform.djhtml")


@app.route("/login")
def login_form():
    return flask.render_template("/registration/login.djhtml")



@app.post("/logout")
def logout():
    flask.session.clear()
    return flask.jsonify({'message': 'You have successfully looged out'}), 200 # noqa: E501
