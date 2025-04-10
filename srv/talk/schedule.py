import json
import pathlib
import flask

from srv import app

FILE = pathlib.Path('schedule.json').resolve()

        
@app.get('/schedule_data')
def schedule_data():
    if FILE.exists():
        with FILE.open() as fp:
            schedule = json.load(fp)
    return flask.jsonify(schedule)
