"""Function handlers for webhook events received by the cloud agent.
"""
import logging
import re

from datacustodian.db import databases, get_view

log = logging.getLogger(__name__)

async def handle_presentations(agent, payload):
    """Handles a presentation webhook event.

    Args:
        agent (CloudAgent): the agent that will handle the event.
        payload (dict): JSON contents of the request.
    """
    state = message["state"]
    presx_id = message["presentation_exchange_id"]

    log.debug(f"Presentation: state=`{state}`; presx_id=`{presx_id}`.")

    _handlers = _presentation_handlers.get(state, {})
    for kind, (rx, h) in _handlers.items():
        m = rx.match(pres_req["name"])
        if m:
            # We only allow a single handler to fire for each event.
            await h(agent, presx_id, payload, m)
            break


async def _presentation_acl_request(agent, presx_id, payload, rx_match=None):
    """Handles a request to compile proof of access for a *specific* CID.

    Args:
        agent (CloudAgent): the agent that will handle the event.
        presx_id (str): identifier for the presentation exchange beween agents.
        payload (dict): the full message received from the other agent.
        rx_match (re.Match): the regex match that triggered calling this handler.
    """
    connection_id = payload["connection_id"]
    connection = await agent.connections.get(connection_id)
    did = connection["their_did"]
    cid = rx_match.groups("cid")

    # Compile a credential set that proves our access to this CID. We select
    # from the many ACL credentials that may match to find the one that has the
    # correct CID.
    query = {
        "cid": cid
    }
    matches = await agent.presentaton.find(presx_id, query=query)
    # Any of these matches are okay because they contain the relevant CID;
    # however, we want to make sure it has the latest issuance date.
    possible = []
    selection = {}
    for match in matches:
        if match["cred_info"]["attrs"].get("cid") != cid:
            continue

        # Since we found one that matches within the time range of the original
        # request, we are good to go. Send the proof back.
        cred_id = match["cred_info"]["referent"]
        selection = {a: cred_id for a in match["cred_info"]["attrs"]}
        break

    if len(selection) > 0:
        r = await agent.presentation.send(presx_id, selection=selection)

        with databases.acl[f"{did}/{cid}"] as doc:
            doc["presentation_exchange_id"] = presx_id
            doc["credential_id"] = cred_id
            doc["attrs"] = list(selection.keys())


async def handle_credentials(agent, payload):
    """Handles a credential webhook event.

    Args:
        agent (CloudAgent): the agent that will handle the event.
        payload (dict): JSON contents of the request.
    """
    state = message["state"]
    credx_id = message["credential_exchange_id"]
    cred_def_id = message["cred_def_id"]

    # Get the credential attributes so that we know how to handle this one.
    attrs = [a for a,b in message["credential_offer"]["key_correctness_proof"]["xr_cap"]]
    log.debug(f"Credential: state=`{state}`; credx_id=`{credx_id}`; attrs=`{attrs}`.")

    _handlers = _credential_handlers.get(state, {})
    for kind, (cattrs, h) in _handlers.items():
        if all(a in attrs for a in cattrs):
            # We only allow a single handler to fire for each event.
            await h(agent, credx_id, payload)
            break


async def _credential_acl_request(agent, credx_id, payload):
    """Handles a request for an ACL credential offer.

    Args:
        agent (CloudAgent): the agent that will handle the event.
        credx_id (str): identifier for the credential exchange beween agents.
        payload (dict): the full message received from the other agent.
    """
    # For an ACL credential offer, we don't know yet what the terms are because
    # the attributes are only provided for key correctness proof. So, we request
    # the actual credential automatically. But, we do not *store* it
    # automatically. If we don't like it later, we can delete it.
    log.debug(f"Sending request for credential details of {credx_id}")
    await agent.credentials.send_request(credx_id)


async def _credential_acl_store(agent, credx_id, payload):
    """Handles an event where a credential was issued and stored for an ACL.

    Args:
        agent (CloudAgent): the agent that will handle the event.
        credx_id (str): identifier for the credential exchange beween agents.
        payload (dict): the full message received from the other agent.
    """
    credential = payload["credential"]
    connection_id = payload["connection_id"]
    connection = await agent.connections.get(connection_id)
    did = connection["their_did"]
    cid = credential["attrs"]["cid"]

    # Add an entry to our database so the UI can be quick.
    with databases.acl[f"{did}/{cid}"] as doc:
        doc["attrs"] = credential["attrs"]
        doc["credential_exchange_id"] = credx_id
        

async def handle_connection(agent, payload):
    """Handles a connection webhook event.

    Args:
        agent (CloudAgent): the agent that will handle the event.
        payload (dict): JSON contents of the request.
    """
    pass


async def handle_basicmessage(agent, payload):
    """Handles a basicmessage webhook event.

    Args:
        agent (CloudAgent): the agent that will handle the event.
        payload (dict): JSON contents of the request.
    """
    pass


handlers = {
    "presentations": handle_presentations,
    "credentials": handle_credentials,
    "connection": handle_connection,
    "basicmessage": handle_basicmessage
}
"""dict: keys are topic names; values are the functions that handle the topic
webhook events.
"""

_presentation_handlers = {
    "request_received": {
        "acl": (re.compile(r"acl:(?P<cid>[\w\d]+)", re.I), _presentation_acl_request)
    }
}
"""dict: keys are `state` values supported by the exchange; values are a `dict`
with a handler name, and a tuple of `(regex, handler)`, where `regex` is a
compiled regular expression to test against the incoming presentation name, and
`handler` is a function to call to handle the request.
"""

_credential_handlers = {
    "offer_received": {
        "acl": (["did","cid","readable","writeable","shareable"], _credential_acl_request),
        "stored": (["did","cid","readable","writeable","shareable"], _credential_acl_store)
    }
}
"""dict: keys are `state` values supported by the exchange; values are a `dict`
with a handler name, and a tuple of `(attrs, handler)`, where `attrs` are a list
of attributes present in the credential offer, and `handler` is the function
to handle the offer.
"""
