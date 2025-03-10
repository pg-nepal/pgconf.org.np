#!venv/bin/python

import os
import argparse
import importlib
import datetime as dt
import json

import srv.pages
import srv.proposals
import srv.attendees
import srv.programs
import srv.reviews
import srv.rates
import srv.dash
import srv.mbox
import srv.tickets

import jinja2

from srv import app


app.jinja_env.globals.update({
    'eventOn_pre' : dt.datetime(2025, 5, 3),
    'eventTo_pre' : dt.datetime(2025, 5, 4),

    'eventOn' : dt.datetime(2025, 5, 5),
    'eventTo' : dt.datetime(2025, 5, 6),
})


def load_config():
    config_dir  = "config"

    for fileName in os.listdir(config_dir):
        if fileName.endswith('.sample.json') or not fileName.endswith('.json'):
            continue

        filePath  = os.path.join(config_dir, fileName)
        configKey = fileName.replace('.json', "")

        try:
            with open(filePath) as FILE:
                print('LOADING CONFIG: {}'.format(filePath))
                app.jinja_env.globals["config"][configKey] = json.load(FILE)
        except json.JSONDecodeError as e:
            print('LOADING CONFIG (ERROR): {}: {}'.format(filePath, str(e)))


def get_sysArgs():
    ap = argparse.ArgumentParser(
        prog        = 'core',
        description = 'services switches',
    )

    ap.add_argument(
        '-d',
        '--debug',
        action  = 'store_true',
        default = bool(os.getenv('DEBUG')),  # non zero length str is True
        help    = 'server on debug-mode',
    )

    ap.add_argument(
        '-u',
        '--unstrict',
        action  = 'store_true',
        default = False,
        help    = 'disable jinja2.strictUndefined in debug mode',
    )

    ap.add_argument(
        '-e',
        '--expose',
        default = 'localhost',
        help    = '0.0.0.0 for exposing beyond local',
    )

    ap.add_argument(
        '-p',
        '--port',
        default = 5000,
        type    = int,
        help    = 'default=5000, use 0 for auto',
    )

    return ap.parse_known_args()


def main():
    sysArgs, keys = get_sysArgs()

    if sysArgs.debug or (sysArgs.unstrict is False):
        srv.app.jinja_env.undefined = jinja2.StrictUndefined

    load_config()

    if sysArgs.debug is False:
        print('live at http://{}:{}'.format(sysArgs.expose, sysArgs.port))
        corn = importlib.import_module('corn')
        corn.Unicorn(
            app  = app,
            host = sysArgs.expose,
            port = sysArgs.port,
        ).run()
    else:
        app.run(
            host  = sysArgs.expose,
            port  = sysArgs.port,
            debug = True,
        )


if __name__ == '__main__':
    main()
