"""Implements a FIDO server for credential registration and authentication. The
credentials are stored for each user in the `couchdb` for the data custodian.
This implementation follows the `webauthn` specification closely: https://www.w3.org/TR/webauthn
"""
from fido2.client import ClientData
from fido2.server import Fido2Server, RelyingParty, ATTESTATION, USER_VERIFICATION, AUTHENTICATOR_ATTACHMENT
from fido2.ctap2 import AttestationObject, AuthenticatorData, AttestedCredentialData
from fido2 import cbor
from urllib.parse import urlparse
from flask import Response
import logging

from datacustodian.utility import import_fqn
from datacustodian.db import get_view
from datacustodian.crypto import bytes_to_b64, b64_to_bytes

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
    rp = RelyingParty(fidoargs["host"],
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


def _get_credentials(did):
    """Retrieves a list of stored credentials (if they exist) for the given DID.
    """
    credentials = []
    with databases.fido[did] as doc:
        if doc.exists():
            raw_credentials = doc.get("credentials", {})

    # Build the credentials from their raw format.
    for credential_id, cred_data in raw_credentials.items():
        log.debug(f"Found credential {credential_id} in database for {did}.")
        credential, _rest = AttestedCredentialData.unpack_from(b64_to_bytes(cred_data))
        credentials.append(credential)

    return credentials


def _get_state(challenge):
    """Returns any stored state for the DID from the database. The specified
    challenge value is used to find the DID and stored state.

    Returns:
        tuple: `(did, state)` with the found DID and the state dictionary. See
        :func:`_store_state`.
    """
    # Find the user/DID that was given the challenge in this request.
    view = get_view("fido", "challenges_view")
    r = view(key=challenge)["rows"]
    assert len(r) > 0
    did = r[0]["value"]

    # Now, lookup the database entry so we can get the state information.
    state = {}
    with databases.fido[did] as doc:
        state["challenge"] = doc["challenge"]
        state["user_verification"] = doc["user_verification"]
    log.debug(f"Found state {state} from database for {did}.")

    return did, state


def _store_state(did, state):
    """Stores the given state to database for the DID.

    Args:
        did (str): decentralized identifier to store under.
        state (dict): with keys `challenge` and `user_verification`.
    """
    with databases.fido[did] as doc:
        doc["challenge"] = state["challenge"]
        doc["user_verification"] = state["user_verification"]
    log.debug(f"{state} saved in FIDO database for {did}.")


def _delete_state(did):
    """Removes the latest state entry for the DID.
    """
    with databases.fido[did] as doc:
        del doc["challenge"]
        del doc["user_verification"]
    log.debug(f"State deleted from FIDO database for {did}.")


def register_begin_options(**kwargs):
    """Returns the registration options for CORS and credentials.
    """
    headers = [
        ("Access-Control-Allow-Headers", "access-control-allow-origin"),
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "post")
    ]
    return Response(headers=headers)


def register_begin(_data=None, _request=None, **kwargs):
    """Handles the initial request to start registration of an authenticator
    for a given user.

    Args:
        _data (dict): user data description following the schema of `FIDOUserData`
            model.
    """
    did = _data["did"]
    credentials = _get_credentials(did)

    registration_data, state = server.register_begin({
        'id': did.encode("ascii"),
        'name': _data["name"],
        'displayName': _data["display_name"],
        'icon': _data["icon"]
    }, credentials, user_verification=user_verification)

    # Since the requester may not have cookies enabled, save the challenge to
    # the database so we can access it on the next request.
    _store_state(did, state)
    log.debug(f"Registration started with data {registration_data}.")

    # Prepare the response as an octet stream; otherwise flask tries to  encode
    # it as JSON.
    result = cbor.encode(registration_data)
    headers = [
        ("Content-Length", str(len(result))),
    ]
    return Response(result,
                    mimetype='application/octet-stream',
                    headers=headers,
                    direct_passthrough=True)

def register_end_options(**kwargs):
    """Returns the registration options for CORS and credentials.
    """
    headers = [
        ("Access-Control-Allow-Headers", "access-control-allow-origin,content-type"),
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "post")
    ]
    return Response(headers=headers)

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

    # See if we have a valid state stored for the challenge.
    did, state = _get_state(client_data.get("challenge"))

    if "localhost" in client_data.data["origin"] and "https://" not in client_data.data["origin"]:
        # This is a hack for local testing to spoof a secure connection.
        client_data.data["origin"] = client_data.data["origin"].replace("http://", "https://")

    log.debug(f"Registration complete triggered with client data: {client_data}.")
    log.debug(f"Attestation accompanying registration complete is {att_obj}.")
    auth_data = server.register_complete(
        state,
        client_data,
        att_obj
    )

    # Store a base-64 encoded version of the credential for the DID.
    credential_id = bytes_to_b64(auth_data.credential_data.credential_id)
    log.debug(f"Storing credential: {credential_id} for {did}.")
    with databases.fido[did] as doc:
        if "credentials" not in doc:
            doc["credentials"] = {}
        doc["credentials"][credential_id] = bytes_to_b64(bytes(auth_data.credential_data))

    result = cbor.encode({'status': 'OK'})
    headers = [
        ("Content-Length", str(len(result))),
    ]
    return Response(result,
                    mimetype='application/octet-stream',
                    headers=headers,
                    direct_passthrough=True)


def authenticate_begin_options(**kwargs):
    """Returns the registration options for CORS and credentials.
    """
    headers = [
        ("Access-Control-Allow-Headers", "access-control-allow-origin"),
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "post")
    ]
    return Response(headers=headers)


def authenticate_begin(_params=None, **kwargs):
    """Starts an authentication session by returning a challenge to the user.
    """
    did = _params["did"]
    credentials = _get_credentials(did)
    if len(credentials) == 0:
        abort(404)

    auth_data, state = server.authenticate_begin(credentials)
    _store_state(did, state)

    result = cbor.encode(auth_data)
    headers = [
        ("Content-Length", str(len(result))),
    ]
    return Response(result,
                    mimetype='application/octet-stream',
                    headers=headers,
                    direct_passthrough=True)


def authenticate_end_options(**kwargs):
    """Returns the registration options for CORS and credentials.
    """
    headers = [
        ("Access-Control-Allow-Headers", "access-control-allow-origin,content-type"),
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "post")
    ]
    return Response(headers=headers)


def authenticate_end(_request=None, **kwargs):
    """Completes an authentication request by validating the user's signature
    on the challenge value.
    """
    data = cbor.decode(_request.get_data())
    credential_id = data["credentialId"]
    client_data = ClientData(data["clientDataJSON"])
    auth_data = AuthenticatorData(data["authenticatorData"])
    signature = data["signature"]
    log.debug(f"Registration complete triggered with client data: {client_data}.")
    log.debug(f"Authenticator accompanying registration complete is {auth_data}.")
    log.debug(f"Signature presented is {signature} for {credential_id}.")

    did, state = _get_state(client_data.get("challenge"))
    credentials = _get_credentials(did)
    if len(credentials) == 0:
        abort(404, f"Could not locate registered credentials for {did}.")

    if "localhost" in client_data.data["origin"] and "https://" not in client_data.data["origin"]:
        # This is a hack for local testing to spoof a secure connection.
        client_data.data["origin"] = client_data.data["origin"].replace("http://", "https://")

    server.authenticate_complete(
        state,
        credentials,
        credential_id,
        client_data,
        auth_data,
        signature,
    )
    _delete_state(did)

    result = cbor.encode({'status': 'OK'})
    headers = [
        ("Content-Length", str(len(result))),
    ]
    return Response(result,
                    mimetype='application/octet-stream',
                    headers=headers,
                    direct_passthrough=True)
