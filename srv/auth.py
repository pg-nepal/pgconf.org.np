from http import HTTPStatus

import os
import flask


bauth = os.getenv('BAUTH')

keys = {
    bauth : 'root',
}


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