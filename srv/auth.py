import os
from http import HTTPStatus

import flask

from srv import app


keys = {
    os.getenv('BAUTH') : 'root',
}

app.jinja_env.globals.update(isAdmin=False)


def isValid(request):
    """
    returns {dict, user-obj} if authorized else None
    """

    auth = request.headers.get('Authorization')
    if auth is None:
        return False

    return keys.get(auth, False)


def respondInValid():
    status = HTTPStatus.UNAUTHORIZED
    response = flask.make_response(status.description, status.value)
    response.headers['WWW-Authenticate'] = 'Basic'
    return response


@app.route('/logout/basic')
def logoutBasic():
    return respondInValid()
