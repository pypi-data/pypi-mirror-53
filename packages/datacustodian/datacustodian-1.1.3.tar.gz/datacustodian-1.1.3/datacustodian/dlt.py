"""
did-reference      = did [ "/" did-path ] [ "?" did-query ] [ "#" did-fragment ]
did                = "did:" method ":" specific-idstring
method             = 1*methodchar
methodchar         = %x61-7A / DIGIT
specific-idstring  = idstring *( ":" idstring )
idstring           = 1*idchar
idchar             = ALPHA / DIGIT / "." / "-"

The [ "/" did-path ] [ "?" did-query ] [ "#" did-fragment ] part of the regex below were pulled from RFC3986 Appendix B
found here https://tools.ietf.org/html/rfc3986#appendix-B
"""
from urllib.parse import urlencode
import logging
import re

log = logging.getLogger(__name__)

agents = None
"""dict: keys are agent names; values are :class:`datacustodian.agent.CloudAgent`.
These are configured at the application level, and then a reference to them is
added here using :func:`configure` to avoid circular imports.
"""
agent_events = None
"""dict: keys are agent names; values are :class:`threading.Event` to track
agent readiness.
"""
method = None
"""str: method to use when creating DID URLs for this application.
"""
databases = None
"""attrdict.AttrDict: databases for application and acl; this variable is set during :func:`configure`.
"""

DID_RE = re.compile(r"""^((did):([a-z\d]+):([:\w.\-=]+))([^?#]*)(?:\?([^#]*))?(?:#(.*))?""")


class Did:
    """Helper class for constructing and parsing DID URLs according to the specifications
    described above.

    Args:
        url (str): a full DID URL to parse attributes from.
        scheme (str): only `did` is currently supported for the scheme.
        method (str): DID method to encode into the URL, for example `dad`.
        vk (str): public key that should appear in the URL.
        query (str or dict): urlencoded query string params, or a `dict` of
            params to encode into a string.
        path (str): path part of the DID URL.
        fragment (str): frament string that appears after the `#` in the URL.
        context (str or list): of `str` values that appear after the `vk` in a
            `:`-separated list.
    """
    def __init__(self, url=None, scheme="did", method=None, vk=None, query=None,
                 path=None, fragment=None, context=None):
        self.__did_reference = url
        self.__did = None
        self.scheme = scheme
        self.method = method
        self.vk = vk
        self.query = query
        self.path = path
        self.fragment = fragment
        self.context = context
        if self.context is not None and not isinstance(self.context, (list, tuple)):
            self.context = [self.context]

        if isinstance(self.query, dict):
            self.query = urlencode(self.query)

        if self.__did_reference is not None:
            self._validate()

    def _extractDidParts(self):
        """
        Parses and saves DID parts from self.__did_reference
        raises ValueError if fails parsing
        """
        matches = DID_RE.match(self.__did_reference)
        if matches:
            self.__did, self.scheme, self.method, self.vk, self.path, self.query, self.fragment = matches.groups()
            cparts = self.vk.split(':')
            self.vk = cparts[0]
            if len(cparts) > 1:
                self.context = cparts[1:]
        else:
            raise ValueError("Could not parse DID.")

        return self

    def _validate(self):
        if not self.__did_reference.startswith("did"):
            raise ValueError("Invalid Scheme Value.")

        self._extractDidParts()

    @property
    def url(self):
        reference = ""
        if self.context is not None:
            reference += f":{':'.join(self.context)}"
        if self.path:
            reference += f"{self.path}"
        if self.query:
            reference += f"?{self.query}"
        if self.fragment:
            reference += f"#{self.fragment}"

        self.__did_reference = "{}{}".format(self.did, reference)

        return self.__did_reference

    @property
    def did(self):
        if self.method is None:
            self.__did = "{}:{}:{}".format(self.scheme, method, self.vk)
        else:
            self.__did = "{}:{}:{}".format(self.scheme, self.method, self.vk)
        return self.__did


async def configure(app_agents, agent_setup, **dltspecs):
    """Performs ledger initialization activities, including registration of
    schemas and credentials. Such registrations only occur if the agent specified
    has the necessary roles.

    Args:
        app_agents (dict): of specifications for agents that will be configured.
        agent_setup (dict): keys are agent names; values are
            :class:`threading.Event` to track agent readiness.
    """
    global agents, method, databases, agent_events
    from datacustodian.db import databases as dcdbs
    agents = app_agents
    agent_events = agent_setup
    method = dltspecs["did"]["method"]
    databases = dcdbs


async def start():
    """Sets up the schemas, credentials etc. that rely on working cloud agents.
    """
    from datacustodian.settings import app_specs
    dltspecs = app_specs["dlt"]
    # Setup the schemas and credentials in the ledger if they don't exist yet. We store the credential identifier
    # and schema identifier in the application database since there isn't currently a way to look up credential
    # definitions using tags/names/etc.
    for schema_name, schema_spec in dltspecs["schemas"].items():
        schema_id = await _verify_schema(schema_name, schema_spec)
        log.info(f"Schema definition for {schema_name} has identifier {schema_id}.")

    for cred_spec in dltspecs["credentials"]:
        cred_name = cred_spec["name"]
        cred_def_id = await _verify_credential(cred_name, cred_spec)
        log.info(f"Credential definition for {cred_name} has identifier {cred_def_id}.")


async def _verify_schema(schema_name: str, schema_spec: dict):
    """Ensures that the schema definition has been registered with the ledger, and that its identifier has been cached
    locally in the application database.

    Args:
        schema_name (str): name given to the schema by the application specification.
        schema_spec (dict): key-value pairs describing the name, version, and attributes to register with the ledger.

    Returns:
        str: the `schema_id` registered with the ledger and stored in local application database.
    """
    if "agent" not in schema_spec:
        return

    dbid = f"schema_def/{schema_name}:{schema_spec['version']}"
    agent = agents[schema_spec["agent"]]
    schema_id = None
    with databases.app[dbid] as doc:
        if "schema_id" not in doc:
            s = await agent.definitions.new_schema(schema_name, schema_spec["version"], schema_spec["attributes"])
            schema_id = s["schema_id"]
            doc["schema_id"] = schema_id
        else:
            schema_id = doc["schema_id"]

    return schema_id


async def _verify_credential(cred_name: str, cred_spec: dict):
    """Ensures that the credential definition exists on the ledger for public credentials, and that the identifier has
    been cached in the application database.

    Args:
        cred_name (str): name of the credential defined in the application specs.
        cred_spec (dict): key-value pairs describing the credential, its schema, tags, etc.
    """
    if "agent" not in cred_spec:
        return

    dbid = f"cred_def/{cred_name}"
    agent = agents[cred_spec["agent"]]
    credential_definition_id = None
    with databases.app[dbid] as doc:
        schema_id = get_schema_id(cred_spec["schema"], cred_spec["version"])
        if "credential_definition_id" not in doc:
            doc.update(await agent.definitions.new_credential(schema_id))
            doc["schema_id"] = schema_id
        elif doc["schema_id"] != schema_id:
            # Since the schema version changed, we need to define a new credential to match it.
            doc.update(await agent.definitions.new_credential(schema_id))
            doc["schema_id"] = schema_id
        credential_definition_id = doc["credential_definition_id"]

        doc["tags"] = cred_spec.get("tags")

    return credential_definition_id


def get_schema_id(schema_name: str, version: str):
    """Retrieves the schema identifier from the application database for the given schema and version.

    Args:
        schema_name (str): name of the schema defined in the application specification.
        version (str): version string for this schema to get.
    """
    dbid = f"schema_def/{schema_name}:{version}"
    result = None
    with databases.app[dbid] as doc:
        if "schema_id" in doc:
            result = doc["schema_id"]

    return result


def get_cred_def_id(cred_name: str):
    """Returns the credential definition id assigned to the credential with
    `cred_name` that was defined in application specs.

    Args:
        cred_name (str): name of the credential assigned by the user in the application specifications.
    """
    dbid = f"cred_def/{cred_name}"
    result = None
    with databases.app[dbid] as doc:
        if "credential_definition_id" in doc:
            result = doc["credential_definition_id"]

    return result
