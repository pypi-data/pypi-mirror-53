#!/usr/bin/python
from {{name}} import run_app
app = run_app(gunicorn=True)

import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems


def number_of_workers():
    """Returns the number of workers to spawn based on the number of CPUs on the
    system.
    """
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def stop_datacustodian(server):
    """Runs the clean-up code for the data custodian app.
    """
    from datacustodian.datacustodian_app import stop
    from datacustodian import get_master_loop
    _loop = get_master_loop()
    stop(None, None, _loop)

def _get_options(app):
    """Grabs options from the application configuration that configure the
    behavior of gunicorn.
    """
    options = {
        "bind": app.config["SERVER_NAME"],
        "workers": number_of_workers(),
        #"worker_class": "gevent",
        "on_exit": stop_datacustodian
    }
    return options

if __name__ == '__main__':
    options = _get_options(app)
    StandaloneApplication(app, options).run()
