import uuid
import pathlib

import flask
import werkzeug.utils
import sqlalchemy as sa

PATH_base = pathlib.Path('./uploads')
PATH_identification = PATH_base / 'identification'
PATH_receipts = PATH_base / 'receipts'


def save(fileData, field):
    fobj = fileData.get()

    if fobj is None:
        return

    filename = fobj.filename
    if filename.endswith(('pdf', 'jpg', 'png')):
        name = werkzeug.utils.secure_filename(filename)
        fullpath = PATH_receipts / name
        fobj(fullpath)
        fullpath.parent.mkdir(parents=True, exist_ok=True)
        return fullpath
