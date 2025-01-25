import uuid
import pathlib

import flask
import werkzeug.utils
import sqlalchemy as sa

PATH_base = pathlib.Path('./uploads')
PATH_identification = PATH_base / 'identification'
PATH_receipts = PATH_base / 'receipts'


def allowed_file(filename):
    return filename.endswith(('pdf', 'jpg', 'png'))
