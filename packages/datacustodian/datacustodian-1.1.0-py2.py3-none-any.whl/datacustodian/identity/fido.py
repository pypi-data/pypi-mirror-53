"""Implements a FIDO server for credential registration and authentication. The
credentials are stored for each user in the `couchdb` for the data custodian.
This implementation follows the `webauthn` specification closely: https://www.w3.org/TR/webauthn
"""
from fido2.client import ClientData
from fido2.server import Fido2Server, RelyingParty, ATTESTATION, USER_VERIFICATION, AUTHENTICATOR_ATTACHMENT
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2 import cbor
from urllib.parse import urlparse
from flask import session, Response
import logging

from datacustodian.utility import import_fqn
from datacustodian.db import get_view

log = logging.getLogger(__name__)

rp = None
"""fido2.server.RelyingParty: as per the FIDO specs, this is an implementation
of the `RelyingParty` interface for FIDO2.
"""
server = None
"""fido2.server.Fido2Server: object that implements the server interface with
methods for registration and authentication that start and then complete (by
validating signatures) the requests.
"""
user_verification = USER_VERIFICATION.PREFERRED
"""fido2.server.USER_VERIFICATION: default enum selection for user verification
type in the FIDO server. One of `discouraged`, `preferred`, or `required`.
"""
authenticator_attachment = None
"""fido2.server.AUTHENTICATOR_ATTACHMENT: default enum selection for authenticator
attachment. One of `platform`, `cross_platform` or `None`.
"""
databases = None
"""attrdict.AttrDict: databases for application, acl and fido; this variable is
set during :func:`configure`.
"""


def configure(servspecs, **fidoargs):
    """Configures the FIDO server and relying party based on the application
    specifications.

    Args:
        servspecs (dict): server specifications that include the host name that
            this data custodian is bound to.
    """
    global rp, server, databases
    # First configure the server name and icon from application specifications.
    url = urlparse(servspecs.SERVER_NAME)
    if '//' in servspecs.SERVER_NAME:
        host, port = url.netloc.split(':')
    else:
        host, port = url.path.split(':')

    rp = RelyingParty(host,
                      fidoargs.get("name", "Data Custodian FIDO Server"),
                      fidoargs.get("icon"))

    # Grab a reference to the databases; this happens now because they wouldn't
    # be initialized on import of the module.
    from datacustodian.db import databases as dcdbs
    databases = dcdbs

    # Next, create a server object to handle verification of signatures etc.
    # according to the FIDO specification.
    verify_origin = None
    if "origin_verifier" in fidoargs:
        fqn = fidoargs["origin_verifier"]
        mod, verify_origin = import_fqn(fqn)

    server = Fido2Server(rp,
                         attestation=fidoargs.get("attestation", ATTESTATION.NONE),
                         verify_origin=verify_origin)

    # Finally, get the default enum values for registration/authentication calls
    # so that we can reuse them later.
    global user_verification, authenticator_attachment
    if "user_verification" in fidoargs:
        user_verification = USER_VERIFICATION(fidoargs["user_verification"])
    if "authenticator_attachment" in fidoargs:
        authenticator_attachment = AUTHENTICATOR_ATTACHMENT(fidoargs["authenticator_attachment"])


def register_begin(_data=None, _request=None, **kwargs):
    """Handles the initial request to start registration of an authenticator
    for a given user.

    Args:
        _data (dict): user data description following the schema of `FIDOUserData`
            model.
    """
    did = _data["did"]
    credentials = []
    with databases.fido[did] as doc:
        if doc.exists():
            credentials = doc.get("credentials", [])

    registration_data, state = server.register_begin({
        'id': did.encode("ascii"),
        'name': _data["name"],
        'displayName': _data["display_name"],
        'icon': _data["icon"]
    }, credentials, user_verification=user_verification)

    # Since the requester may not have cookies enabled, save the challenge to
    # the database so we can access it on the next request.
    with databases.fido[did] as doc:
        doc["challenge"] = state["challenge"]
        doc["user_verification"] = state["user_verification"]
    log.debug(f"Registration started with data {registration_data}.")
    log.debug(f"{state} saved in FIDO database for {did}.")

    # Prepare the response as an octet stream; otherwise flask tries to  encode
    # it as JSON.
    result = cbor.encode(registration_data)
    headers = [
        ('Content-Length', str(len(result))),
        ('Access-Control-Allow-Origin', '*')
    ]
    return Response(result,
                    mimetype='application/octet-stream',
                    headers=headers,
                    direct_passthrough=True)

def register_end(_request=None, **kwargs):
    """Handles the `/complete` request to finalize registration of a credential
    for a user-authenticator pair.
    """
    data = cbor.decode(_request.get_data())

    # These next lines follow the spec closely; it defines special data formats
    # where each bit has specific meaning to keep the data as small as possible.
    client_data = ClientData(data['clientDataJSON'])
    att_obj = AttestationObject(data['attestationObject'])
    log.debug(f"Registration complete triggered with client data: {client_data}.")
    log.debug(f"Attestation accompanying registration complete is {att_obj}.")

    # Find the user/DID that was given the challenge in this request.
    view = get_view("fido", "challenges_view")
    r = view(key=client_data.get("challenge"))["rows"]
    assert len(r) > 0
    did = r[0]["value"]
    # Now, lookup the database entry so we can get the state information.
    state = {}
    with databases.fido[did] as doc:
        state["challenge"] = doc["challenge"]
        state["user_verification"] = doc["user_verification"]

    auth_data = server.register_complete(
        state,
        client_data,
        att_obj
    )

    #credentials.append(auth_data.credential_data)
    log.debug('Storing credential:', auth_data.credential_data)
    return cbor.encode({'status': 'OK'})

def authenticate_begin():
    pass

def authenticate_end():
    pass
