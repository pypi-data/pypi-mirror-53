"""Functions to enabled consent management: offers, sharing, revocation, etc.
that is backed by DLT.
"""
import json, logging
from datetime import datetime
from werkzeug.exceptions import Conflict, Forbidden
from flask import Response

from datacustodian.db import databases, package, get_view
from datacustodian.dlt import agents, get_cred_def_id, Did
from datacustodian.crypto import (sign, derived_keypair, create_keypair, random_seed, create_did,
                                  bytes_to_b64, b64_to_bytes)
from datacustodian.utility import AwareJSONEncoder, datetime_to_str
from datacustodian.agent.presentation import create_referent

from .circles import get_did_for_circle
from .auth import expand_did
from .files import serve

log = logging.getLogger(__name__)

def get_did_for_cid(cid):
    """Makes sure the DID document data entries that will enable DID resolution
    for the data shared in a particular grant exist.

    .. note:: If a DID and DDO already exist for the CID being shared and the
        DID of the entity receiving access, then this method will just return
        the DID URL.

    Args:
        cid (str): IPFS CID of the data that is being shared.

    Returns:
        tuple: `(seed, DID, verkey)` for the CID being shared with the entity in `grant`.
    """
    # We index grant information in the ACL database to store DID/DDO related
    # items needed by the endpoint that resolves the DID URLs.
    with databases.acl[cid] as doc:
        if "seed" not in doc or doc["seed"] is None:
            # Create a new did for the CID.
            doc["seed"] = bytes_to_b64(random_seed())
            did, verkey = create_did(doc["seed"])
            doc["did"] = did
            doc["verkey"] = verkey
            log.debug(f"Created new DID: {did} and verkey: {verkey} for CID `{cid}`.")
        result = doc["seed"], doc["did"], doc["verkey"]

    return result

async def access(_data=None, _agent=None, **kwargs):
    """Verifies that the requester has access to the CID in `_data` using the
    verifiable credential in the presentation exchange.
    """
    agent = agents[_agent]
    cid, did = _data["cid"], _data["did"]
    presx_id = None

    with databases.acl[f"{did}/{cid}"] as doc:
        presx_id = doc["presentation_exchange_id"]

    ok = False
    if presx_id is not None:
        ok = await agent.presentation.verify(presx_id)
    if not ok:
        raise Forbidden(f"Credential for CID {cid} is not valid.")

    obj = serve(cid)
    headers = [
        ('Content-Length', str(len(obj))),
        ('Content-Disposition', 'attachment; filename="/ipfs/%s"' % cid),
    ]

    log.debug("Responding with headers=%r for %s.", headers, cid)
    return Response(obj,
                    mimetype='application/octet-stream',
                    headers=headers,
                    direct_passthrough=True)

async def proof(_data=None, _agent=None, **kwargs):
    """Constructs a proof request so that the actual presential credential can
    be provided in the request for the shared data.

    Args:
        _data (dict): values conforming to the model `ProofRequest`.
    """
    agent = agents[_agent]
    cid, did = _data["cid"], _data["did"]
    presx_id = None

    with databases.acl[f"{did}/{cid}"] as doc:
        presx_id = doc.get("presentation_exchange_id")

    if presx_id is not None:
        result = await agent.presentation.get(presx_id)
        return result["presentation_request"]

    with databases.acl[cid] as doc:
        cid_did = doc["grants"][did]["did"]

    # Construct the list of referents that should be proved for the access. We
    # need access to the cred_def_id to ensure that it matches our credential.
    # Since the system allows sharing with provenance, we don't demand that we
    # are the issuer.
    end_date = _data.get("end")
    attributes = ["readable", "writeable", "shareable", "semop_schema",
                  "fields", "priors", "signature", "did"]
    referents = {}

    for attr in attributes:
        referents[attr] = create_referent(attr, cred_def_id=cred_def_id, end=end_date)
    # Don't know if `==` is supported; it would be great if it is; otherwise
    # we have to choose from the list of matching credentials on the other side.
    # referents["did"] = create_referent("did", operator="==", value=cid_did, cred_def_id=cred_def_id)

    connections = await agent.connections.ls(state="active", their_did=did)
    assert len(connections) > 0
    connection_id = connections[0]["connection_id"]

    f = agent.presentation.send_request
    request = await f(connection_id, f"acl:{cid}", "0.0", referents.values())

    with databases.acl[f"{did}/{cid}"] as doc:
        doc["cred_def_id"] = cred_def_id
        doc["presentation_exchange_id"] = request["presentation_exchange_id"]

    return request["presentation_request"]


async def grant(_data=None, _agent=None, **kwargs):
    """Grants access to data for a given circle.

    Args:
        circle (str): name of the circle to grant access to.
        _data (dict): ACL for granting the access. See the model for
            `Grant`.
    """
    cred_data = {
        "cid": _data["cid"],
        "semop_schema": "acl-0.0"
    }
    cid_seed, cid_did, cid_verkey = get_did_for_cid(_data["cid"])
    json_fields = ["shareable", "fields", "priors"]
    for field in json_fields:
        if field in _data:
            cred_data[field] = json.dumps(_data[field], cls=AwareJSONEncoder)
        else:
            cred_data[field] = ""

    o_fields = ["readable", "writeable"]
    for field in o_fields:
        if field in _data:
            cred_data[field] = "true" if _data[field] else "false"
        else:
            cred_data[field] = "false"

    # We need the definition of the credential and the schema before we can
    # issue any credentials. These definitions can be reused for each of the
    # new issuances.
    agent = agents[_agent]
    cred_def_id = get_cred_def_id(_data["credential_name"])

    public = _data.get("public", False)
    did_list = []
    from_circle, circle_did = False, None
    if _data.get("circle") is not None:
        circle_did = get_did_for_circle(_data["circle"])
        did_list = expand_did(circle_did)
        from_circle = True
    elif len(_data.get("grantees",[])) > 0:
        did_list = _data["grantees"]

    #Count the number of grants, issuances, revocations attached to the CID
    #already.
    n_grants = 0
    with databases.acl[_data["cid"]] as doc:
        if "grants" in doc:
            n_grants += len(doc["grants"])
            n_grants += sum(len(d) for d in doc["issuance_history"])
            n_grants += sum(len(d) for d in doc["revocation_history"])

    #Count the number of ACL records present in the database so far.
    n_recs = len(databases.acl.db)

    result = []
    didpath = "/grants"
    context = _data["cid"]
    log.debug(f"Granting access to {context} for {did_list}.")
    for did in did_list:
        if did == circle_did:
            # The circle did is included in its expanded list of dids, but it
            # isn't a valid connection to share data with.
            continue

        with databases.acl[_data["cid"]] as doc:
            if "grants" not in doc:
                doc["grants"] = {}
                doc["issuance_history"] = {}
                doc["revocation_history"] = {}

            #See if we are updating an existing credential. If so, keep track
            #of previous issuances.
            if did in doc["grants"]:
                if _data.get("replace", False):
                    i = doc["issuance_history"].get(did, [])
                    i.append(doc["grants"][did])
                    doc["issuance_history"][did] = i
                else:
                    raise Conflict("Grant already exists and `replace` was not specified.")

            # We need to generate a deterministic key path so that we can generate
            # a derived key for this sharing operation. The public part of the
            # dDID will be from `agent` wallet; the path needs the integer ordering
            # of the circle and grantee.
            cred_copy = cred_data.copy()
            n_grants += 1
            keypath = f"/0/{n_recs}/{n_grants}"
            vk, pk, sk = derived_keypair(_agent, b64_to_bytes(cid_seed), context, keypath)
            cred_did = Did(vk=cid_verkey, query={"chain": keypath}, path=didpath)
            cred_copy["did"] = cred_did.url

            # Next, append the signature for all the preceding data to the credential
            # data dictionary. This has to be done for each member of the circle
            # independently so that we have provenance for the data sharing.
            contents = json.dumps(cred_copy)
            cred_copy["signature"] = sign(contents, sk)

            # Finally, send a credential offer to the connection that controls this did.
            connections = await agent.connections.ls(state="active", their_did=did)
            assert len(connections) > 0
            connection_id = connections[0]["connection_id"]

            log.debug(f"Sending credential offer to {connection_id} as {cred_copy}.")
            credx = await agent.credentials.send(cred_def_id, connection_id, cred_copy)
            result.append({
                "grantee_did": did,
                "credential_exchange_id": credx["credential_exchange_id"],
                "did": cred_copy["did"]
            })
            log.debug(f"Grant for {did} has info {result[-1]}.")

            doc["grants"][did] = {
                "credential_exchange_id": credx["credential_exchange_id"],
                "did": cred_copy["did"],
                "issued": datetime_to_str(datetime.utcnow()),
                "public": public
            }
            if from_circle:
                doc["grants"][did]["circle"] = _data["circle"]

    return result


async def get(grant_did=None, _agent=None, **kwargs):
    """Retrieves the details of an access grant. Since the access grant is
    itself just a credential, this just pulls up the data associated with
    the credential granted under `grant_did`, which is itself the
    `credential_id`.

    Args:
        grant_did (str): DID of the grant to retrieve. This is the URL included
            in the issued credential for a specific connection.
    """
    # First, we need to get the credential_id so that we can load the details
    # of the credential from the agent API.
    assert grant_did is not None
    view = get_view("consent", "grant_view")
    r = view(key=grant_did)["rows"]
    assert len(r) > 0
    entry = r[0]
    did = entry["value"]

    with databases.acl[entry["id"]] as doc:
        if did in doc["grants"]:
            result = doc["grants"][did]
        elif did in doc["revocation_history"]:
            result = doc["revocation_history"][did]
        elif did in doc["issuance_history"]:
            result = doc["issuance_history"][did]

    credx_id = result["credential_exchange_id"]
    agent = agents[_agent]
    credx = await agent.credentials.exchange_get(credx_id)
    result.update(credx["credential_values"])
    result["credential_definition_id"] = credx["credential_definition_id"]
    result["schema_id"] = credx["schema_id"]

    json_fields = ["shareable", "fields", "priors"]
    for field in json_fields:
        if field in result:
            result[field] = json.loads(result[field])

    return result


def revoke(_data=None, **kwargs):
    """Revokes access to data for a given circle or list of dids.

    Args:
        circle (str): name of the circle to revoke access from.
        _data (dict): details for revoking the access. See the model for
            `GrantRevocation`.
    """
    if _data.get("circle") is not None:
        circle_did = get_did_for_circle(_data["circle"])
        did_list = expand_did(circle_did)
        from_circle = True
    if len(_data.get("revokees",[])) > 0:
        did_list.extend(_data["revokees"])

    for did in set(did_list):
        if did == circle_did:
            continue

        with databases.acl[_data["cid"]] as doc:
            if "grants" not in doc:
                break

            if did in doc["grants"]:
                c = doc["revocation_history"].get(did, [])
                d = doc["grants"][did]
                d["revoked"] = datetime_to_str(datetime.utcnow())
                c.append(d)
                doc["revocation_history"][did] = c
                del doc["grants"]


def _search_status(rdict, doc, status):
    """Includes the relevant entries from `doc` in the resulting `rdict` only
    if the status matches.

    .. warning:: `rdict` is modified by this function.
    """
    if status is None or status == "issued":
        rdict["issued"] = doc.get("issuance_history")
    if status is None or status == "revoked":
        rdict["revoked"] = doc.get("revocation_history")
    if status is None or status == "active":
        rdict["active"] = doc.get("grants")


_end_time = 10413817200.0
"""float: timestamp representing Jan 1, 2300 as the maximum end date for missing
filter comparisons on datetime.
"""
def _compare_shareable(a, b):
    """Compares serialized version `a` of the `Provenance` model for similarity
    with `dict` `b` that follows the `ProvenanceFilter` model.
    """
    da = json.loads(a)
    return (da["delegate_read"] == b.get("delegate_read", False) and
            da["delegate_write"] == b.get("delegate_read", False) and
            da["delegate_read"] == b.get("delegate_read", False) and
            da["read_expires"] < b.get("read_expires_start", 0) and
            da["read_expires"] < b.get("read_expires_end", _end_time) and
            da["write_expires"] < b.get("write_expires_start", 0) and
            da["write_expires"] < b.get("write_expires_end", _end_time) and
            da["share_expires"] < b.get("share_expires_start", 0) and
            da["share_expires"] < b.get("share_expires_end", _end_time))


_grant_filter = {
    "fields": lambda g, f: (any(_ in f.get("fields_included", []) for _ in g["fields"]) or
                            all(_ not in f.get("fields_excluded", []) for _ in g["fields"])),
    "expiration": lambda g, f: (g["issued"][1].timestamp() > f.get("expiration_start", 0) and
                                g["issued"][1].timestamp() < f.get("expiration_end", _end_time)),
    "readable": lambda g, f: g["readable"] == f.get("readable", False),
    "writeable": lambda g, f: g["writeable"] == f.get("writeable", False),
    "shareable": lambda g, f: _compare_shareable(g["shareable"], f.get("shareable", {}))
}


def _filter_grants(grants, filters):
    """Filters the set of grants to return only those that match the filters.

    Args:
        grants (list): of `dict` that match the model `Grant`.
        filters (dict): that matches the model `GrantFilter`.
    """
    result = []
    fkeys = list(filters.keys())
    for grant in grants:
        #Check all the filters for which values were actually supplied.
        keep = all(v(grant, filters) for k, v in _grant_filter.items()
                   if k in fkeys)
        if keep:
            result.append(grant)
    return result


async def _compile_grants(metagrants, _agent):
    """Compiles the full grant definition by requesting the credential data
    referenced in the `metagrant` that is stored in the ACL database.

    Args:
        metagrants (dict): keys are `did`, values are either a `dict` or a list
            of `dict` with the credential issuance/history information.
        _agent (str): name of the configured agent to query credential data with.

    Returns:
        list: of compiled grants that follow the `Grant` model.
    """
    if metagrants is None:
        return []

    agent = agents[_agent]
    result = []
    for did, detail in metagrants.items():
        if isinstance(detail, dict):
            entries = [detail]
        else:
            entries = detail

        for meta in entries:
            credx_id = meta["credential_exchange_id"]
            credx = await agent.credentials.exchange_get(credx_id)
            meta.update(credx["credential_values"])
            meta["credential_definition_id"] = credx["credential_definition_id"]
            meta["schema_id"] = credx["schema_id"]
            result.append(meta)

    return result


async def search(_data=None, _agent=None, **kwargs):
    """Searches all grants that a data custodian has given.

    .. note:: Search functionality is controlled by the `GrantFilter` model,
        which is included in the request JSON.

    Args:
        _data (dict): details for filter the grant list. See the model for
            `GrantFilter`.
        _agent (str): name of the configured agent to query credential data with.
    """
    matches = {}
    cids = _data.get("cids", []) or []
    status = _data.get("status")

    # First, collect the explicit CIDs in the filter.
    for cid in _data["cids"]:
        matches[cid] = {
            "issued": None,
            "revoked": None,
            "active": None
        }
        with databases.acl[cid] as doc:
            if doc.exists():
                _search_status(matches[cid], doc, status)

    # Next, check the circle membership or explicit grantees did lists.
    did_list = []
    if _data.get("circle") is not None:
        circle_did = get_did_for_circle(_data["circle"])
        did_list.extend(expand_did(circle_did))
    if _data.get("dids") is not None:
        did_list.extend(_data["dids"])

    if len(did_list) > 0:
        view = get_view("consent", "did_view")
        r = view(keys=did_list)["rows"]
        for entry in r:
            if status is None or r["value"] == status:
                cid = entry["id"]
                if cid in matches:
                    continue
                else:
                    matches[cid] = {
                        "issued": None,
                        "revoked": None,
                        "active": None
                    }

                with databases.acl[cid] as doc:
                    _search_status(matches[cid], doc, status)

    # Now, filter these document results by the rest of the attributes specified
    # in the filter.
    result = {}
    for cid, acls in matches.items():
        for k in acls:
            grants = await _compile_grants(acls[k], _agent)
            result[k] = _filter_grants(grants, _data)

    return result
