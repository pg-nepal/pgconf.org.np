import flask

import srv.auth

from srv import app


@app.get('/proposals/<int:pk>')
def proposal_read_view(pk):
    isAdmin = srv.auth.isValid(flask.request)
    if isAdmin is False:
        return srv.auth.respondInValid()

    return flask.render_template(
        '/proposals/read.djhtml',
        isAdmin = isAdmin,
        pk      = pk,
    )
