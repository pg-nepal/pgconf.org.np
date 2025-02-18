import flask
import jinja2


app = flask.Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.undefined = jinja2.StrictUndefined


class CustomJSONEncoder(flask.json.provider.DefaultJSONProvider):
    sort_keys = False


app.json = CustomJSONEncoder(app)
