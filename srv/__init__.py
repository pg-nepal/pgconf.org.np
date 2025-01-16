import os
import secrets
import datetime as dt

import flask
import jinja2
from flask_jwt_extended import JWTManager


DURATION  = dt.timedelta(hours=1)
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_bytes(16).hex())
print(SECRET_KEY)
KHALTI_API_KEY = os.getenv('KHALTI_API_KEY')
KHALTI_API_URL = os.getenv('KHALTI_API_URL')
print(KHALTI_API_KEY)
print(KHALTI_API_URL)

app = flask.Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.undefined = jinja2.StrictUndefined
app.secret_key = SECRET_KEY
app.khalti_key = KHALTI_API_KEY
app.khalti_url = KHALTI_API_URL

app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = DURATION
app.config["KHALTI_KEY"] = KHALTI_API_KEY
app.config["KHALTI_URL"] = KHALTI_API_URL

jwt = JWTManager(app)
