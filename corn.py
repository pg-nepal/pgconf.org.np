import os

import gunicorn.app.base


class Unicorn(gunicorn.app.base.BaseApplication):
    def __init__(self, app, host, port, workers=None, reload=False):
        self.host    = host
        self.port    = port
        self.reload  = reload
        cpu = os.cpu_count() or 1
        self.workers = workers or (cpu * 2)

        super().__init__()
        self.application = app

    #
    def load_config(self):
        self.cfg.set('bind', '{}:{}'.format(self.host, self.port))
        self.cfg.set('workers', self.workers)
        self.cfg.set('reload', self.reload)

    #
    def load(self):
        return self.application
