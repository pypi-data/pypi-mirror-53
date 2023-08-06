"""Starts an instance of Aries cloud agent to interact with the configured DLT.
Currently, ACA only supports `indy` ledger, but they have designed their API
to be DLT-agnostic, so it will be able to support other ledger kinds in the
future.
"""
from os import environ
from typing import Sequence
from argparse import ArgumentParser
import asyncio
import functools
import logging
import json
import subprocess
from aiohttp import web, ClientSession, ClientRequest, ClientError

from datacustodian.utility import flatten
from datacustodian import msg
from datacustodian.base import SectionProperty

from . import wallet, credentials, server, connections, definitions, presentation, menu, ledger
from .handlers import handlers

log = logging.getLogger(__name__)

start_secs = ["admin", "debug", "general", "ledger", "logging", "protocol",
              "transport", "wallet"]
"""list: of `str` section names supported in the DLT agent configuration for
the `start` command.
"""
provision_secs = ["general", "logging", "wallet", "ledger"]
"""list: of `str` section names supported in the DLT agent configuration for
the `provision` command.
"""
aca_x = "aca-py"
"""str: path to the `aca-py` executable on the local system. If it is on the
`$PATH` (expected default), then its name is good enough.
"""

async def execute(argv: Sequence[str] = None):
    """Copy of :func:`aries_cloudagent.commands.provision.execute` so that we
    don't get conflicts with event loops that are already running.
    """
    from aries_cloudagent.config.util import common_config
    from aries_cloudagent.commands.provision import init_argument_parser, provision
    parser = ArgumentParser()
    parser.prog += " provision"
    get_settings = init_argument_parser(parser)
    args = parser.parse_args(argv)
    settings = get_settings(args)
    common_config(settings)
    await provision(settings)

def _bool_cast(v):
    """Determines if the specified value is a boolean or common boolean string.
    """
    if isinstance(v, bool):
        return True, v
    if isinstance(v, str) and v.lower() in ["true", "false", 't', 'f']:
        return True, v.lower() in ["true", 't']
    return False, False

async def genesis_txns(genesis_file=None, genesis_url=None):
    """Retrieves the genesis transactions from either a file or a URL.

    Args:
        genesis_file (str): path to the genesis file, which should have the
            transactions as valid JSON inside.
        genesis_url (str): URL to a web server that hosts the genesis transactions
            at the `/genesis` endpoint; for example, the web server that ships
            with `von-network`.
    """
    genesis = None
    try:
        if genesis_url is not None:
            async with ClientSession() as session:
                async with session.get(genesis_url) as resp:
                    genesis = await resp.text()
        elif genesis_file is not None:
            with open(genesis_file, "r") as f:
                genesis = f.read()
    except Exception:
        log.error("Error loading genesis transactions.", exc_info=True)
    return genesis

class CloudAgent(object):
    """Represents a cloud agent subprocess hosting an instance of the Aries
    cloud agent.

    Args:
        dltspecs (dict): key-value pairs that configure the agent.

    Attributes:
        args (list): of command-line arguments that will be passed to the
            `aca-py` executable.
        proc (subprocess.Popen): subprocess running the cloud agent endpoints.
        client_session (aiohttp.ClientSession): asynchronous session client for
            making requests to the agents endpoints.
        hostname (str): name of the host to use as a public endpoint. Usually
            passed in as the docker `hostname`.
        webhook_url (str): URL to the endpoint accepting webhook requests.
        webhook_port (int): port to use for the webhook site.
        webhook_site (web.TCPSite): actual site running the webhook request and
            response logic.
        admin_url (str): URL to direct admin-based HTTP requests.
        endpoint (str): external URL for the endpoint that faces the world.
        terminating (bool): when True, the :meth:`terminate` has been called
            and all the dependencies are cleaning up.

    Examples:

        Assuming that the specifications are available in a `dltspecs` variable:

        >>> agent = CloudAgent(**dltspecs)
        >>> await agent.listen_webhooks(8022)
        >>> await agent.start_process()
    """
    wallet       = SectionProperty(wallet.Section)
    credentials  = SectionProperty(credentials.Section)
    server       = SectionProperty(server.Section)
    connections  = SectionProperty(connections.Section)
    definitions  = SectionProperty(definitions.Section)
    presentation = SectionProperty(presentation.Section)
    menu         = SectionProperty(menu.Section)
    ledger       = SectionProperty(ledger.Section)

    def __init__(self, agent_name=None, hostname=None, webhook_port=None, **dltspecs):
        self.agent_name = agent_name
        self.dltspecs = dltspecs
        self.start_args = None
        self.provision_args = None
        self.proc = None
        self.hostname = hostname
        self.webhook_port = webhook_port
        self.webhook_url = None
        self.webhook_site = None
        self.endpoint = dltspecs["transport"]["endpoint"]
        self.terminating = False
        self.api_key = dltspecs["admin"].get("admin-api-key")

        headers = None
        if self.api_key is not None:
            headers = {"x-api-key": self.api_key}
        self.client_session = ClientSession(headers=headers)

        #Build the admin_url from DLT specs.
        host, port = dltspecs["admin"]["admin"]
        self.admin_url = f"http://{host}:{port}"

    async def configure(self, start=True):
        """Parses the configuration specifications from the `dlt` section of the
        application spec files. Creates the default command arguments string
        to start the cloud agent.

        Args:
            start (bool): when True, configure the arguments for the *start*
                command; otherwise for the provision command.
        """
        args = []
        sections = start_secs if start else provision_secs
        for section in sections:
            s = self.dltspecs.get(section, {})
            for argname, argvalue in s.items():
                if argvalue is None:
                    continue

                # Pad the given seed to be 32 bytes long, if necessary.
                if argname == "seed":
                    # Get the value of the seed from an environment variable.
                    envseed = environ[argvalue]
                    argvalue = f"{envseed:0>32}"
                if argname  == "genesis-transactions":
                    argvalue = await genesis_txns(argvalue)

                is_bv, bv = _bool_cast(argvalue)
                if is_bv:
                    if bv:
                        args.append(f"--{argname}")
                elif isinstance(argvalue, dict):
                    args.append((f"--{argname}", json.dumps(argvalue)))
                elif isinstance(argvalue, (list, tuple)):
                    args.append((f"--{argname}",) + tuple(map(str, argvalue)))
                else:
                    args.append((f"--{argname}", argvalue))

        if start:
            self.start_args = args
        else:
            self.provision_args = args

    def handle_output(self, output, source: str = None):
        """Handles output to the screen with colors.

        Args:
            output (BytesIO): usually the object returned from the
                :class:`subprocess.PIPE` for `stdout` and `stderr`.
            source (str): one of `stdout` or `stderr`, which sets the coloring
                of the output to console.
        """
        while not self.terminating:
            text = output.readline().strip()
            if len(text) > 0:
                if "INFO" in text:
                    source = "stdout"
                elif "ERROR" in text:
                    source = "stderr"
                elif "WARNING" in text:
                    source = "warn"

                if source == "stderr":
                    msg.err(text)
                elif source == "warn":
                    msg.warn(text)
                elif not source:
                    msg.info(text)
                else:
                    msg.std(text)

    async def provision_wallet(self):
        """Calls the `provision` command of the cloud agent to initialize the
        wallet for this agent.
        """
        log.info(f"Provisioning agent wallet for {self.agent_name}.")
        await self.configure(start=False)
        agent_args = list(flatten([self.provision_args]))
        log.debug("Executing provision with %r", agent_args)
        await execute(agent_args)

    def _process(self, args, env, loop):
        """Opens the actual cloud agent subprocess.

        Args:
            args (list): of command-line arguments to use to invoke the process.
            env (dict): shell environment variables to set.
            loop (asyncio.AbstractEventLoop): the event loop running the main
                application from which to spawn additional thread executors.
        """
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            encoding="utf-8",
        )
        #IMPORTANT: the process that gets created here will keep listening and
        #processing requests until it is terminated. The `stdout` and `stderr`
        #pipes will thus also exist for the full duration. As such, they need
        #to be run in their own threads that keep monitoring and messaging using
        #our custom handler; otherwise, they will block the event loop running
        #this main application.
        loop.run_in_executor(None, self.handle_output, proc.stdout, "stdout")
        loop.run_in_executor(None, self.handle_output, proc.stderr, "stderr")
        log.debug("Finished setting up `stdout` and `stderr` in agent startup.")
        return proc

    async def start_process(self, wait=True):
        """Starts the cloud agent process using configured specifications.

        Args:
            wait (bool): when True, block the thread until the agent endpoints
                are up and running.
        """
        #We need to make sure the wallet is available before we do everything
        #else. This is especially true when the wallet hasn't been initialized
        #yet. Instead of checking for existence, and then initializing, we just
        #call 'provision', which checks for wallet existence before doing anything.
        await self.provision_wallet()

        log.info(f"Starting cloud agent with admin url at {self.admin_url}, "
                 f"and externally facing endpoint at {self.endpoint}.")
        env = environ.copy()
        await self.configure()
        agent_args = list(flatten([aca_x, "start", self.start_args]))
        log.debug("Running cloud agent using %r", agent_args)

        # Start agent sub-process in a separate thread.
        loop = asyncio.get_event_loop()
        self.proc = await loop.run_in_executor(
            None, self._process, agent_args, env, loop
        )
        log.debug(f"Executor completed; cloud agent {self.agent_name} is running.")
        if wait:
            await self.detect_process()

    async def detect_process(self):
        """Detects whether the swagger API of the cloud agent is up and running,
        which indicates that the agent is ready to receive requests.
        """
        text = None
        for i in range(10):
            if self.terminating:
                break
            # wait for process to start and retrieve swagger content
            await asyncio.sleep(2.0)
            try:
                aurl = f"{self.admin_url}/api/docs/swagger.json"
                log.debug("Testing client API readiness at %s.", aurl)
                async with self.client_session.get(aurl) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        break
            except ClientError as ce:
                text = None
                continue

        if not self.terminating:
            if not text:
                raise Exception(f"Timed out waiting for agent process to start")
            if "Aries Cloud Agent" not in text:
                raise Exception(f"Unexpected response from agent process")

        # Set the thread synchronizing event that this agent is ready.
        from datacustodian.dlt import agent_events
        agent_events[self.agent_name].set()

    def _terminate(self):
        """Termines the subprocess hosting the cloud agent.
        """
        if self.proc and self.proc.poll() is None:
            log.debug("Attempting termination of cloud agent subprocess.")
            self.proc.terminate()
            try:
                self.proc.wait(timeout=0.5)
                log.info(f"Exited cloud agent with return code {self.proc.returncode}")
            except subprocess.TimeoutExpired:
                msg = "Cloud agent process did not terminate in time."
                log.debug(msg)
                raise Exception(msg)

    async def terminate(self):
        """Terminates the subprocess hosting the cloud agent, the asynchronous
        session client, and the webhook site that this agent is using.
        """
        log.info(f"Terminating cloud agent at {self.admin_url} and {self.endpoint}.")
        self.terminating = True
        loop = asyncio.get_event_loop()
        if self.proc:
            await loop.run_in_executor(None, self._terminate)
        log.debug("Closing async client session gracefully.")
        await self.client_session.close()
        if self.webhook_site:
            log.debug("Closing webhook site gracefully.")
            await self.webhook_site.stop()
        self.terminating = False

    async def listen_webhooks(self):
        """Sets this agent up to listen for webhooks and then execute those
        requests using the appropriate handler instance method on this object.

        Args:
            webhook_port (int): port to use in configuring the webhook site.
        """
        if self.webhook_port is None:
            raise ValueError("Webhook port is not configured for agent.")

        self.webhook_url = f"http://{self.hostname}:{str(self.webhook_port)}/webhooks"
        app = web.Application()
        app.add_routes([web.post("/webhooks/topic/{topic}/", self._receive_webhook)])
        runner = web.AppRunner(app)
        log.debug("Setting up app runner for webhooks site.")
        await runner.setup()
        self.webhook_site = web.TCPSite(runner, self.hostname, self.webhook_port)
        log.debug("Starting webhook site at %s.", self.webhook_url)
        await self.webhook_site.start()

    async def _receive_webhook(self, request: ClientRequest):
        """Webhook request handler that extracts the JSON payload, triggers the
        handling of the request with the appropriate instance method, and then
        sends a canned response.
        """
        topic = request.match_info["topic"]
        payload = await request.json()
        log.debug("Received webhook at topic %s with payload %r.", topic, payload)
        await self.handle_webhook(topic, payload)
        return web.Response(text="")

    async def handle_webhook(self, topic: str, payload):
        """Automatically configures this agent to handle webhook requests by
        calling the appropriate method of this instance object.

        Args:
            topic (str): topic of the section in the OpenAPI that should be
                handled. For example `connections`.
            payload (dict): the JSON payload that was included in the web request.
        """
        if topic != "webhook":  # would recurse
            method = handlers.get(topic)
            if method:
                await method(self, payload)

    async def admin_request(self, method, path, data=None, as_text=False,
                            params=None, **kwargs):
        """Performs an asynchronous HTTP request to the admin endpoint for
        the given method and arguments.

        Args:
            method (str): one of the HTTP methods to use.
            path (str): relative path in the OpenAPI to send the request to.
            data (dict): payload to send with the request in the `json` argument.
            as_text (bool): when True, return the response as a `str`; otherwise,
                return the deserialized JSON `dict`.
            params (dict): URL parameters to send with the request.
        """
        log.debug(f"Making admin endpoint request for {method.upper()} to "
                  f"{self.admin_url + path}.\n{data}\n{params}")
        async with self.client_session.request(
            method, self.admin_url + path, json=data, params=params, **kwargs
        ) as resp:
            if resp.status < 200 or resp.status > 299:
                raise Exception(f"Unexpected HTTP response: {resp.status}")
            if as_text:
                r = await resp.text()
            else:
                r = await resp.json()
            log.debug(f"Response from {self.admin_url} is {r}.")
            return r
