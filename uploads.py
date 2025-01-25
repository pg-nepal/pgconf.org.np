import pathlib

import flask

from srv import app


PATH_base = pathlib.Path('./srv/uploads/receipts').resolve()


@app.route('/uploads/attendees/<filename>')
def file_srv(filename):
    return flask.send_from_directory(PATH_base, filename)


@app.route('/uploads/attendees/receipt/<filename>')
def files_srv_receipt(filename):
    return flask.send_from_directory(PATH_base, filename, as_attachment=True)  # noqa:E501
