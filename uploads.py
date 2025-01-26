import pathlib

import flask
import werkzeug.utils

from srv import app


PATH_base = pathlib.Path('./srv/uploads/receipts').resolve()


def save(fileData, field):
    fobj = fileData.get(field)

    if fobj is None:
        return

    filename = fobj.filename
    if filename.endswith(('pdf', 'jpg', 'png')):
        name = werkzeug.utils.secure_filename(filename)
        fullpath = PATH_base / name
        fullpath.parent.mkdir(parents=True, exist_ok=True)
        fobj.save(str(fullpath))
        return str(fullpath)


@app.route('/uploads/attendees/<filename>')
def file_srv(filename):
    return flask.send_from_directory(PATH_base, filename)


@app.route('/uploads/attendees/receipt/<filename>')
def files_srv_receipt(filename):
    return flask.send_from_directory(PATH_base, filename, as_attachment=True)  # noqa:E501
