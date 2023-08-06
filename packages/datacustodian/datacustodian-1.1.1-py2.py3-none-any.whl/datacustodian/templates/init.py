# Auto-generated package module by :mod:`datakeeper`.
import logging
import asyncio
import signal
from os import path, environ
log = logging.getLogger(__name__)
reporoot = path.abspath(path.expanduser(environ.get("{{ name | upper }}_HOME", '.')))
log.info("Using %s as the home directory for {{ name }}.", reporoot)

from datacustodian.utility import relpath


def run_app(norun=False, start_agents=False, gunicorn=False):
    """Runs the application in the current event loop; schedules cleanup of the
    the loop when the app exits.
    """
    from datacustodian.datacustodian_app import run
    log.info("Initializing API with specifications at %r", appspecs)
    try:
        app = run(appspecs=appspecs, norun=norun, start_agents=start_agents, gunicorn=gunicorn)
    except:
        log.exception("Initializing app from package.")
    log.debug(f"Run app call finished with result {app}.")
    return app

appspecs = [relpath(s, reporoot) for s in {{ appspecs }}]
{%- if autoload %}
app = run_app()
{%- endif %}


async def get_client(host="localhost", agent=None, api_key=None, timeout=20.):
    """Returns an HTTP client that can interact with these auto-generated
    endpoints.

    Args:
        host (str): HTTP hostname of the data custodian that this client will
            be interacting with.
        agent (str): name of the configured agent to use for cryptographic
            operations. This is required if the endpoints need did-based
            authentication.
        api_key (str): API key to use in the request header.
        timeout (float): number of seconds to wait for cloud agent to initialize
            before failing HTTP client creation.
    """
    from .client import HTTPClient
    result = HTTPClient(host, agent, api_key)
    if await result.detect_agent():
        log.info("Found a running data custodian with cloud agent.")
        # We still need to initialize the specifications and objects though.
        run_app(norun=True, start_agents=False)
        return result
    else:
        # We only need to start the cloud agents for the client to work properly.
        log.info("Starting a new data custodian and cloud agent instance.")
        run_app(norun=True, start_agents=True)

    # Before we return the client, we need to make sure the agent is up and
    # running; otherwise none of the crypto functionality will work.
    from datacustodian import application_ready
    wait_count = 0
    ready = application_ready()
    while not ready and wait_count < int(timeout/2.) + 1:
        await asyncio.sleep(2.)
        wait_count += 1

    if ready and await result.detect_agent():
        return result
    else:
        log.error("Could not initilize client because cloud agent isn't ready.")
