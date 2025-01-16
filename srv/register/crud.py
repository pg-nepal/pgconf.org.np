import db
import db.events
import flask
import sqlalchemy as sa
import uuid

import srv.auth
from srv import app


@app.get("/register/form")
def register_form():
    return flask.render_template("/register/form.djhtml")


@app.get("/register/payment")
def payment_form():
    return flask.render_template("/register/payment.djhtml")


@app.get("/root/register")
def register_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(db.events.Register)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        "/register/list.djhtml", cursor=cursor, isAdmin=isAdmin
    )


@app.post("/register/add")
def register_create():
    formdata = flask.request.form.to_dict()

    query = sa.insert(db.events.Register).values(
        **formdata,
        registration_id=str(uuid.uuid4()),
        fee=1000,
        status="pending",
        ticket="ticket",
    )

    with db.SessionMaker.begin() as session:
        cursor = session.execute(query)
        id = cursor.inserted_primary_key[0]
        return flask.redirect(f"/register/{id}")


@app.get("/root/register/<int:pk>")
def register_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.events.Register,
    ).where(
        db.events.Register.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return "Invalid pk", 400

        return flask.render_template(
            "/register/read.djhtml",
            row=row,
            isAdmin=isAdmin,
        )


@app.get("/register/<int:pk>")
def register_read_client(pk):
    query = sa.select(
        db.events.Register,
    ).where(
        db.events.Register.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.first()

        if row is None:
            return "Invalid pk", 400

        return flask.render_template("/register/profile.djhtml", row=row)


@app.delete("/register/<int:pk>")
def register_delete(pk):
    with db.SessionMaker.begin() as session:
        session.execute(
            sa.delete(
                db.events.Register,
            ).where(
                db.events.Register.pk == pk,
            )
        )

    return flask.jsonify({"message": "Registration deleted successfully"}), 202
