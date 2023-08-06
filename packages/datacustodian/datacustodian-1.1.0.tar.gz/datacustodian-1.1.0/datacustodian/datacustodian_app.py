#!/usr/bin/python
import logging.config
import argparse
import signal
import threading
import asyncio
from os import path, makedirs
from flask import Flask, Blueprint
from threading import Event
from flask_cors import CORS
from functools import partial

from datacustodian.base import testmode
from datacustodian.settings import load, specs, app_specs
from datacustodian import msg
from datacustodian.utility import relpath, import_fqn
from datacustodian.base import bparser, exhandler
from datacustodian.api import create_api, ServerThread
from datacustodian.writers import component_write
from datacustodian.ipfs import configure as configure_ipfs
from datacustodian.agent import CloudAgent
from datacustodian.db import configure as configure_db, cleanup as cleanup_db
from datacustodian.dlt import configure as configure_dlt, start as start_dlt
from datacustodian.consent.auth import configure as configure_auth
from datacustodian.identity.fido import configure as configure_fido

app = None
"""flask.Flask: for the overall application.
"""
apis = {}
"""dict: keys are component names; values are the :class:`flask_restplus.Api`
instances for the component.
"""
server = None
"""datacustodian.api.ServerThread: server for the REST API.
"""
agents = {}
"""dict: keys are agent names; values are :class:`datacustodian.agent.CloudAgent`
instances.
"""
loop = None
"""AbstractEventLoop: main loop for the application.
"""
started = Event()
"""threading.Event: synchronizer indicating that initial startup methods have
been called.
"""
app_inited = Event()
"""threading.Event: set when the flask app has been initialized completely
(meaning that it is ready to have `run` called).
"""

logging.config.fileConfig(relpath('datacustodian/templates/logging.conf'))
log = logging.getLogger(__name__)


def set_loop(l):
    """Sets the application event loop to use.
    """
    global loop
    loop = l

    log.debug("Setting event_loop for component modules.")
    package = app_specs["package"].name
    for compname in specs:
        fqn = "{}.{}.set_event_loop".format(package, compname)
        mod, obj = import_fqn(fqn)
        log.debug(f"Setting event_loop for {fqn} using {obj}.")
        obj(loop)


def examples():
    """Prints examples of using the script to the console using colored output.
    """
    script = "DataCustodian REST API for Local Node"
    explain = ("This scripts starts a REST API on the local machine for each "
               "of the application configuration specifications. See examples "
               "in `docs/configs/*.yml`.")
    contents = [(("Start the local REST API server for two applications."),
                 "app.py records.yml consent.yml",
                 "Each application will run on the same port, but under a "
                 "different URL prefix, as specified in the configuration for the app.")]
    required = ("'app.yaml' file with REST application configuration.")
    output = ("")
    details = ("")
    outputfmt = ("")

    msg.example(script, explain, contents, required, output, outputfmt, details)


script_options = {
    "appspecs": {"help": "File containing the root endpoint specifications.",
                 "nargs": '+'},
    "--overwrite": {"help": ("Recreate generated *module* files from scratch."
                             "This does *not* overwrite any package files, "
                             "like setup.py, __init__.py, etc. Use "
                             "--reset-package to do that."),
                    "action": "store_true"},
    "--generate": {"help": ("Generate the package code; when not specified, "
                            "only the server will run on existing code."),
                   "action": "store_true"},
    "--reset-package": {"help": ("Recreates package files like setup.py, "
                                 "__init__.py, conftest.py from scratch. This nukes "
                                 "*your* changes to the files!"),
                        "action": "store_true"},
    "--norun": {"help": "Don't start the application server.",
                "action": "store_true"},
    "--nowait": {"help": ("Don't wait until the agents are up and running before "
                          "starting the API server."),
                 "action": "store_true"}
}
"""dict: default command-line arguments and their
    :meth:`argparse.ArgumentParser.add_argument` keyword arguments.
"""


def _parser_options():
    """Parses the options and arguments from the command line."""
    pdescr = "Data Custodian REST API"
    parser = argparse.ArgumentParser(parents=[bparser], description=pdescr)
    for arg, options in script_options.items():
        parser.add_argument(arg, **options)

    args = exhandler(examples, parser)
    if args is None:
        return

    return args


def _get_subspec(key, d, ref=None, source=None):
    """Retrieves a sub-specification from the `d`

    Args:
        key (str): name of the attribute to retrieve, if it exists.
        d (dict): specification dictionary to check attributes for.
        ref: if specified and not `None`, then a warning will be printed that
            the attribute is being overridden.
        source (str): source of `d` to use in the warning message if generated.

    Returns:
        The reference object `ref` if the key does not exist; this avoids
        overwriting previous specs that were good with `None`.
    """
    log.debug(f"Found specification for {key}.")
    if key in d:
        if ref is not None:
            wmsg = "{} specification is overridden by {}"
            log.warning(wmsg.format(key.capitalize(), source))
        # We use the getattr call here so that a :class:`AttrDict` is returned
        # regular key access returns a regular dict.
        return getattr(d, key)
    else:
        return ref

def stop(signal, frame, _loop=None):
    """Stops the application server and cloud agents.

    Args:
        _loop (asyncio.AbstractEventLoop): master event loop to stop the
            dependencies with.
    """
    from datacustodian import stop_all_loops
    global server
    msg.okay("SIGINT >> cleaning up API server and cloud agents.", -1)

    try:
        if server is not None:
            server.shutdown()
        future = asyncio.run_coroutine_threadsafe(async_stop(_loop), _loop)
        future.add_done_callback(stop_all_loops)

        log.debug("Cleaning up database connections.")
        cleanup_db()

        if not future.done():
            future.result(5)
    except:
        log.exception("Shutting down application.")
        exit()

async def async_stop(_loop):
    from datacustodian import stop_all_loops
    global agents
    for agent_name, agent in agents.items():
        log.debug(f"Calling terminate for agent `{agent_name}`")
        await agent.terminate()

    log.debug("Shutting down async generators for main application thread.")
    s = _loop.shutdown_asyncgens()
    await s

async def start(nowait=False, norun=False, start_agents=False):
    """Starts the server for the application.

    .. note:: If `start_agents=True`, then the agents will start even if
        `norun=True`.

    Args:
        nowait (bool): when True, just start all the servers, don't wait for
            the agents to be up and running before starting the API server.
        norun (bool): when True, no servers or agents are started, only
            configuration of event loops is attempted. See the note above.
        start_agents (bool): when True, start the agents even if `norun=False`.
    """
    global agents, started

    log.debug("Starting cloud agents: %r", list(agents.keys()))
    for agent_name, agent in agents.items():
        if (not norun) or start_agents:
            await agent.listen_webhooks()
            await agent.start_process(not nowait)
    log.debug("Finished initializing cloud agents.")

    # When the agents are up and running, we can start the API server.
    from datacustodian.dlt import agent_events
    if not norun and agent_events is not None:
        for agent_name, event in agent_events.items():
            log.debug(f"Waiting for cloud agent {agent_name} to startup.")
            event.wait(10)

    # Now, setup the DLT schemas and credentials, etc.
    if not norun and "dlt" in app_specs:
        lob.debug("Starting DLT ledger setup routines.")
        await start_dlt()

    log.debug("Finished starting dependencies; setting started Event flag.")
    started.set()


async def _setup(appspecs=None, generate=False, overwrite=False, reset_package=False,
                 debug=False, norun=False, nowait=False, start_agents=False, **args):
    """Sets up all necessary dependencies for the main REST application.
    """
    if appspecs is None:
        return

    # Read the global application specification recursively
    srvspec, packspec, appspec, ipfsspec = None, None, None, None
    dltspec, dbspec, authspec, fidospec, corsspec = None, None, None, None, None

    for compfile in appspecs:
        aspec = load(compfile)
        srvspec = _get_subspec("server", aspec, ref=srvspec, source=compfile)
        packspec = _get_subspec("package", aspec, packspec, compfile)
        appspec = _get_subspec("app", aspec, appspec, compfile)
        ipfsspec = _get_subspec("ipfs", aspec, ipfsspec, compfile)
        dltspec = _get_subspec("dlt", aspec, dltspec, compfile)
        dbspec = _get_subspec("db", aspec, dbspec, compfile)
        authspec = _get_subspec("auth", aspec, authspec, compfile)
        fidospec = _get_subspec("fido", aspec, authspec, compfile)
        corsspec = _get_subspec("cors", aspec, authspec, compfile)

        if "components" in aspec:
            for compspec in aspec.components:
                specs[compspec.name] = compspec

    if corsspec is not None:
        app_specs["corrs"] = corsspec
    if srvspec is not None:
        app_specs["server"] = srvspec

    app_specs["app"] = appspec
    app_specs["package"] = packspec

    # Configure the application overrides folder. This folder stores specific
    # configuration attribute overrides for different components/modules.
    app_specs["overrides"] = relpath(path.expanduser(appspec.overrides), '.')
    if not path.isdir(app_specs["overrides"]):
        makedirs(app_specs["overrides"])

    # If there is an IPFS spec for the cluster, configure the cluster.
    if ipfsspec is not None:
        log.debug("Configuring IPFS with %r", ipfsspec)
        app_specs["ipfs"] = ipfsspec
        configure_ipfs(norun=norun, **ipfsspec)

    if dbspec is not None:
        log.debug("Configuring CouchDB with %r", dbspec)
        app_specs["db"] = dbspec
        configure_db(packspec, norun=norun, **dbspec)

    if fidospec is not None:
        log.debug("Configuring FIDO with %r", fidospec)
        app_specs["fido"] = fidospec
        configure_fido(srvspec, **fidospec)

    if dltspec is not None:
        app_specs["dlt"] = dltspec

        global agents
        agent_setup = {}
        for agent_name, agent_spec in dltspec["agents"].items():
            log.debug("Creating cloud agent '%s' from specs.", agent_name)
            agent = CloudAgent(agent_name=agent_name, **agent_spec)
            agents[agent_name] = agent
            agent_setup[agent_name] = Event()

        # Next, initialize the ledger schemas, cred_defs, etc.
        await configure_dlt(agents, agent_setup, **dltspec)

    # Auth initialization depends on the databases having already been
    # initialized; that's why this is here.
    if authspec is not None:
        configure_auth(norun=norun, **authspec)
        app_specs["auth"] = authspec

    await start(norun=norun, start_agents=start_agents)
    return True


def _configure_app(generate=False, overwrite=False, reset_package=False,
                   testing=False, debug=False, appspecs=None):
    """Configures the flask application according to specifications parsed by
    :func:`_setup`.
    """
    global app
    app = Flask('datacustodian.app')

    # Apply the relevant configuration sections to the application object.
    if "server" in app_specs:
        srvspec = app_specs["server"]
        log.debug(f"Flask application configuration set to {srvspec}.")
        app.config.update(srvspec)

    if "corrs" in app_specs:
        corsspec = app_specs["corrs"]
        log.debug(f"Configure CORS using {corsspec}.")
        cors = CORS(app, **corsspec)

    # Now, iterate over the components defined for the application and create
    # a python namespace for each, then configure them on the global flask
    # application object at their registered URL prefixes.
    appspec = app_specs["app"]
    packspec = app_specs["package"]
    log.debug(f"Using {appspec} for application specs.")
    log.debug(f"Found {list(specs.keys())} components in the application spec.")
    root = path.abspath(path.expanduser(packspec.root))
    for compname, compspec in specs.items():
        # Create the API object to connect the component to. It is cached in
        # datacustodian.api and datacustodian.app
        log.debug(f"Creating API for component {compspec.name}.")
        api = create_api(appspec, compspec)
        apis[compspec.name] = api
        if generate:
            log.debug(f"Generating code file for {compspec.name}.")
            component_write(appspecs, packspec, compspec, overwrite=overwrite,
                            reset=reset_package, allspecs=specs)
        if testing:
            # Make sure that a second call without overwrite enabled triggers the
            # right logic paths in the code.
            component_write(appspecs, packspec, compspec, overwrite=False, reset=False, allspecs=specs)

        # Import the blueprint object that has been initialized for the component.
        fqn = "{}.{}.blueprint".format(packspec.name, compname)
        log.debug(f"Dynamically importing {fqn}.")
        mod, obj = import_fqn(fqn, folder=root)
        log.debug("Registering blueprint %r from %s.", obj, fqn)
        app.register_blueprint(obj)

    app.debug = appspec.get("debug", False) or debug
    return app

def init_flask_app(future, generate=False, overwrite=False, reset_package=False,
                   testing=False, debug=False, appspecs=None, _loop=None):
    """Calls :meth:`Flask.run` to start the web server in the current thread.

    Args:
        future (asyncio.Future): whose result is the initialized flask application
            from another thread.
    """
    global app
    log.debug("Running callback for flask application configuration and start, "
              f"generate={generate}; overwrite={overwrite}; reset_package={reset_package}; "
              f"testing={testing}; debug={debug}; appspecs={appspecs}.")
    try:
        app = _configure_app(generate, overwrite, reset_package, testing, debug, appspecs)
        setup_ok = future.result()
    except:
        log.exception("While configuring flask app and dependencies.")
        setup_ok = False

    # Wait for the dependencies to initialize all the way.
    if not setup_ok:
        stop(None, None, _loop=_loop)
        return
    started.wait()

    # Now, make sure the endpoints have access to the event loop.
    set_loop(_loop)
    app_inited.set()
    log.debug("App initialization complete.")
    return app

def run(**args):
    """Initializes the REST application with all configured component endpoints.
    """
    from datacustodian import create_loops
    log.debug(f"Running data custodian with CLI args as {args}.")
    create_loops()

    # Now that the loop has been created and is running, import it for use here.
    from datacustodian import get_master_loop
    _loop = get_master_loop()
    _testing = args.get("testing", False)
    stopper = partial(stop, _loop=_loop)
    if not _testing and not args.get("gunicorn", False):
        # We only setup these handlers explicitly if gunicorn is not running;
        # otherwise it is handled in the exit routine of gunicorn.
        signal.signal(signal.SIGINT, stopper)
        signal.signal(signal.SIGTERM, stopper)

    # Schedule execution of application startup in a separate thread.
    kwargs = {k: args.get(k, False) for k in ["testing", "generate", "overwrite", "reset_package", "debug", "appspecs"]}
    cb = partial(init_flask_app, _loop=_loop, **kwargs)
    future = asyncio.run_coroutine_threadsafe(_setup(**args), _loop)
    future.add_done_callback(cb)

    # Finally, start the flask app. It should have been configured already
    # with all the application specs.
    app_inited.wait()
    if __name__ == "__main__" and not args.get("norun", False):
        global server
        server = ServerThread(app, app_specs["server"].SERVER_NAME)
        server.start()
    else:
        if __name__ == "__main__":
            log.debug("Stopping API server for `--norun`.")
            stop(None, None, _loop)
        else:
            log.debug(f"Returning {app} since not running __main__.")
            return app

if __name__ == '__main__':  # pragma: no cover
    args = _parser_options()
    app = run(**args)
