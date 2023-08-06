"""Functions to support DID registration, signatures, provenance, etc. for
identity-based operations.
"""
from datacustodian.dlt import agents, Did

async def agent_ready(_agent=None, **kwargs):
    """Tests if the specified agent is ready to accept requests.
    """
    agent = agents[_agent]
    try:
        await agent.detect_process()
        ready = True
    except:
        ready = False

    return {
        "agent": _agent,
        "ready": ready
    }

async def register(did: str = None, verkey: str = None, alias: str = None,
                   role: str = None, _agent=None):
    """Registers a new DID on the ledger.

    .. note:: This request establishes a new identity on the ledger. Based
        on the `role`, the new identity may be able to establish additional
        identities. Possible `role` values are:

        - `None` (common USER)
        - TRUSTEE
        - STEWARD
        - TRUST_ANCHOR
        - ENDORSER - equal to TRUST_ANCHOR that will be removed soon
        - NETWORK_MONITOR
        - empty string to reset role

    Args:
        did (str): DID to register on the public ledger.
        verkey (str): corresponding verkey for `did`.
        alias (str): human-friendly alias to assign to the DID.
        role (str): see the note above about roles.
    """
    assert did is not None and verkey is not None
    agent = agents[_agent]
    await agent.ledger.register_nym(did, verkey, alias, role)
