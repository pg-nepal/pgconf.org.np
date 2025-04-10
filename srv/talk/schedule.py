import sys
import json
import pathlib
import flask

from srv import app

FILE = pathlib.Path('schedule.json').resolve()

if FILE.exists():
    print('# Loading schedule from: {}'.format(FILE), file=sys.stderr)
    with FILE.open() as fp:
        schedule = json.load(fp)

        
@app.get('/schedule_data')
def schedule_data():
    if FILE.exists():
        with FILE.open() as fp:
            schedule = json.load(fp)
    return flask.jsonify(schedule)
