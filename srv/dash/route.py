import flask

import srv.auth
import srv.dash.reports
from srv import app


@app.get('/dash')
@app.get('/admin')
@app.get('/organizer')
@srv.auth.auth_required()
def dash_index():
    return flask.render_template(
        '/dash/main.djhtml',
        isAdmin = srv.auth.loggedInUser(flask.request),
        registration_tickets_status = srv.dash.reports.get_registration_tickets_status(),
        registration_payment_status = srv.dash.reports.get_registration_payment_status(),
        accepted_proposals = srv.dash.reports.get_accepted_proposals(),
    )
