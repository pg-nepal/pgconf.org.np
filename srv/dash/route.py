import flask

import srv.auth

from srv import app


@app.get('/dash')
@app.get('/admin')
@app.get('/organizer')
def dash_index():
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/dash/main.djhtml',
        isAdmin = isAdmin,
    )
