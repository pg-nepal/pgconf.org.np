import os
import secrets
import datetime as dt

import flask
import jinja2
from flask_jwt_extended import JWTManager


DURATION  = dt.timedelta(hours=1)
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_bytes(16).hex())
print(SECRET_KEY)

app = flask.Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.undefined = jinja2.StrictUndefined
app.secret_key = SECRET_KEY

app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = DURATION

jwt = JWTManager(app)
