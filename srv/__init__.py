import enum
import decimal as d
import datetime as dt

import flask
import jinja2


app = flask.Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.undefined = jinja2.StrictUndefined

# better defaults
app.jinja_env.globals['config'] = {
    'analytics' : {},
}


class CustomJSONEncoder(flask.json.provider.DefaultJSONProvider):
    sort_keys = False

    def default(self, obj):
        if isinstance(obj, dt.date)  : return obj.isoformat()
        if isinstance(obj, dt.time)  : return obj.isoformat()
        if isinstance(obj, enum.Enum): return obj.name
        if isinstance(obj, d.Decimal): return float(obj)

        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return tuple(iterable)

        return super().default(obj)


app.json = CustomJSONEncoder(app)
