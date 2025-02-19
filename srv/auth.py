import os
import sys
import json
import pathlib
from functools import wraps
from http import HTTPStatus

import flask

from srv import app


keys = {
    os.getenv('BAUTH') : 'root',
}

FILE = pathlib.Path('users.json').resolve()
if FILE.exists():
    print('# Loading users from: {}'.format(FILE), file=sys.stderr)
    with FILE.open() as fp:
        keys.update(json.load(fp))


app.jinja_env.globals.update(isAdmin=False)


def isValid(request):
    """
    returns {dict, user-obj} if authorized else None
    """

    auth = request.headers.get('Authorization')
    if auth is None:
        return False

    return keys.get(auth, False)


def isLoggedIn(request): # replacement of isValid
    auth = request.headers.get('Authorization')
    if auth is None: return False
    return True if keys.get(auth,False) else False


def loggedInUser(request):
    auth = request.headers.get('Authorization')
    if auth is None:
        return False
    return keys.get(auth, False)


def respondInValid():
    status = HTTPStatus.UNAUTHORIZED
    response = flask.make_response(status.description, status.value)
    response.headers['WWW-Authenticate'] = 'Basic'
    return response


def auth_required(role='admin'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            isAuthorized = isLoggedIn(flask.request)
            if not isAuthorized:
                return respondInValid()
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/logout/basic')
def logoutBasic():
    return respondInValid()
