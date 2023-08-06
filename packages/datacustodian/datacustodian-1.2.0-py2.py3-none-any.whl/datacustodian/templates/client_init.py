"""Auto-generated HTTP client that can consume the auto-generated endpoints
created by `datacustodian`.
"""
from aiohttp import ClientSession
from contextlib import asynccontextmanager
import logging
import asyncio

from datacustodian.base import SectionProperty

log = logging.getLogger(__name__)
{%- for compname, compspec in compspecs.items() %}
{%- for nspec in compspec.namespaces %}
from .{{ compname }} import {{ nspec.name|title }}Section
{%- endfor %}
{%- endfor %}

class HTTPClient(object):
    """An HTTP Client for accessing the endpoints exposed by this package.

    Args:
        host (str): HTTP hostname of the data custodian that this client will
            be interacting with.
        agent (str): name of the configured agent to use for cryptographic
            operations. This is required if the endpoints need did-based
            authentication.
        api_key (str): API key to use in the request header.

    Attributes:
        client_session (aiohttp.ClientSession): asynchronous session client for
            making requests to the agents endpoints.
        terminating (bool): when True, the client has been requested to terminate.
    """
    {%- for compname, compspec in compspecs.items() %}
    {%- for nspec in compspec.namespaces %}
    {{ nspec.name }} = SectionProperty({{ nspec.name|title }}Section)
    {%- endfor %}
    {%- endfor %}

    def __init__(self, host=None, agent=None, api_key=None):
        from datacustodian.consent.auth import get_signed_headers
        self.agent = agent
        self.api_key = api_key
        self.host = host
        self.terminating = False
        self.signer = get_signed_headers

        headers = None
        if self.api_key is not None:
            headers = {"x-api-key": self.api_key}
        self.client_session = ClientSession(headers=headers)

    async def terminate(self):
        """Terminates the asynchronous session client.
        """
        log.info(f"Terminating HTTP client for {self.host}.")
        self.terminating = True
        await self.client_session.close()

    async def detect_agent(self):
        """Detects whether the cloud agent is up and running,
        which indicates that the agent is ready to receive requests.
        """
        readiness = None
        for i in range(10):
            if self.terminating:
                break
            # wait for process to start and retrieve swagger content
            await asyncio.sleep(2.0)
            try:
                aurl = f"{self.host}/id/did/agent"
                log.debug("Testing cloud agent readiness at %s.", aurl)
                async with self.client_session.get(aurl) as resp:
                    if resp.status == 200:
                        readiness = await resp.json()
                        log.debug(f"Got OK response with {readiness}.")
                        break
            except ClientError as ce:
                readiness = None
                continue

        if not self.terminating:
            if not readiness:
                raise Exception(f"Timed out waiting for API endpoint to respond.")
            if not readiness["ready"]:
                raise Exception(f"Endpoint active, but not cloud agent.")

        return True


    @asynccontextmanager
    async def request(self, method, path, data=None, as_text=False,
                      params=None, didauth=False, **kwargs):
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
        url = self.host + path
        headers = None
        if didauth:
            headers = await self.signer(self.agent, url, method)
            log.debug(f"`didauth` headers added: {headers}")

        log.debug(f"Making admin endpoint request for {method.upper()} to "
                  f"{url}.\n{data}\n{params}")
        async with self.client_session.request(
            method, url, json=data, params=params, headers=headers, **kwargs
        ) as resp:
            if resp.status < 200 or resp.status > 299:
                contents = await resp.content.read()
                raise Exception(f"Unexpected HTTP code: {resp.status} > {contents}.")
            if as_text:
                t = "`text`"
                r = resp.text()
            else:
                if "json" in resp.content_type :
                    t = "`json`"
                    r = resp.json()
                else:
                    t = "`binary`"
                    r = resp.content
            log.debug(f"{t} response from {self.host}.")
            yield r
