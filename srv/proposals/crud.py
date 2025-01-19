import db
import db.proposals
import flask
import sqlalchemy as sa
import random

import srv.auth
from srv import app

# from flask_jwt_extended import jwt_required, get_jwt_identity

questions = [
    ("What is used to retrieve data from a database?", "SELECT"),
    ("What is used to remove data from a table?", "DELETE"),
    ("What command is used to modify data in a table?", "UPDATE"),
    ("What is used to sort data in SQL?", "ORDER"),
    ("What SQL keyword is used to combine results from two or more tables?", "JOIN"),
]

@app.get("/proposals/form")
def proposal_form():

    question, answer = random.choice(questions)

    flask.session['captcha_answer'] = answer

    return flask.render_template(
        "/proposals/form.djhtml",
        question=question
    )

@app.post("/proposals/add")
# @jwt_required()
def proposal_create():
    formdata = flask.request.form.to_dict()
    captcha_answer = formdata.get('wtf-answer', '')
    correct_answer = flask.session.get('captcha_answer')

    if captcha_answer != correct_answer:
        flask.flash("Your answer: ",captcha_answer)
        return flask.jsonify({"error": "Incorrect answer. Please try again."}), 400

    formdata.pop("wtf-answer", None)

    formdata['session_id'] = flask.session['session_id']

    try:

        query = sa.insert(db.proposals.Proposals).values(**formdata)

        with db.SessionMaker.begin() as session:
            session.execute(query)

        return flask.redirect("/call_for_proposal")

    except Exception as e: 
        return flask.jsonify({"error": str(e)}), 400        

@app.get("/root/proposals")
def proposal_list():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(db.proposals.Proposals)

    with db.engine.connect() as connection:
        cursor = connection.execute(query)

    return flask.render_template(
        "/proposals/list.djhtml",
        cursor=cursor,
        isAdmin=isAdmin,
    )

@app.get("/root/proposals/<int:pk>")
def proposal_read(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    query = sa.select(
        db.proposals.Proposals,
    ).where(
        db.proposals.Proposals.pk == pk,
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query)
        row = cursor.mappings().first() if cursor else None

    if row is None:
        return "Invalid Pk", 400

    return flask.render_template(
        "/proposals/read.djhtml",
        proposal=row
    )

@app.get("/proposals/status/<string:session_id>")
def check_proposal(session_id):

    query = sa.select(
        db.proposals.Proposals
        ).where(
        session_id==session_id
        )

    with db.engine.connect() as connection:
        proposal = connection.execute(query).first()
        # proposal = cursor._asdict()

    if proposal:
        return flask.jsonify({"status": "exists", "message": "The proposal exist"})
    else:
        return flask.jsonify({"status": "not_exists", "message": "The proposal does not exist"})

@app.get("/proposals/<string:session_id>")
def client_proposal_read(session_id):

    query = sa.select(
        db.proposals.Proposals,
    ).where(
        db.proposals.Proposals.session_id == session_id
    )

    with db.engine.connect() as connection:
        cursor = connection.execute(query).first()
        row = cursor._asdict() if cursor else None

    if row is None:
        return flask.jsonify({"error": "Invalid session ID"}), 400

    return flask.jsonify(row)

@app.post("/proposals/update/<int:pk>")
def proposal_update(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()
        
    data = flask.request.form
    query = (
        sa.update(
            db.proposals.Proposals
        )
        .where(
            db.proposals.Proposals.pk == pk
        )
        .values(
            **data,
            updatedBy = 'dummy'
        )
    )

    print(query)

    with db.SessionMaker.begin() as session:
        session.execute(query)

    return flask.redirect(flask.url_for('proposal_list'))

@app.post("/proposals/<string:session_id>")
def client_proposal_update(session_id):
    data = flask.request.form
    query = (
        sa.update(
            db.proposals.Proposals
        )
        .where(
            db.proposals.Proposals.session_id == session_id
        )
        .values(
            **data,
            updatedBy = 'dummy'
        )
    )

    print(query)

    with db.SessionMaker.begin() as session:
        session.execute(query)

    return flask.redirect(flask.url_for('proposal_read'), pk=pk)

@app.delete("/root/proposals/delete/<int:pk>")
def proposal_delete(pk):
    with db.SessionMaker.begin() as session:
        session.execute(
            sa.delete(
                db.proposals.Proposals,
            ).where(
                db.proposals.Proposals.pk == pk,
            )
        )

    return flask.jsonify({"message": "Proposal deleted successfully"}), 202
