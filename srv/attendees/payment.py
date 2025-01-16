import flask

from srv import app


@app.get('/attendees/payment')
def payment_form():
    return flask.render_template(
        '/attendees/payment.djhtml',
    )
