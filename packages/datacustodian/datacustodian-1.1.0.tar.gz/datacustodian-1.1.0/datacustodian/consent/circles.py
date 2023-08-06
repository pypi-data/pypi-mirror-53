"""Handles CRUD operations for circles and the membership within each circle.
"""
from fnmatch import fnmatch

from datacustodian.db import databases, package, get_view
from datacustodian.datacustodian_app import agents
from .auth import verify_roles, set_did, rm_did

def get_did_for_circle(circle):
    """Returns the DID associated with `circle`.

    Args:
        circle (str): name of the circle to retrieve a DID for.
    """
    dbid = f"circle/{circle}"
    with databases.app[dbid] as doc:
        result = doc["did"]
    return result

async def update(circle=None, _data=None, _agent=None, **kwargs):
    """Creates/updates a circle with the given name if it doesn't already exist.

    Args:
        circle (str): name of the circle to create.
        _data (dict): configuration details for the circle; follows the schema
            of model `Circle`.
        _agent (str): name of the agent to use for did-based authentication.
    """
    dbid = f"circle/{circle}"
    add, rm = None, None
    with databases.app[dbid] as doc:
        doc["roles"] = _data["roles"]
        if "did" not in doc or doc["did"] is None:
            #Create a new did for the circle so that its can be referenced by
            #the auth system.
            ndid = await agents[_agent].wallet.create()
            did, verkey = ndid["did"], ndid["verkey"]
            doc["did"] = did
            doc["verkey"] = verkey
        else:
            did = doc["did"]

        if "members" not in doc:
            doc["members"] = []

        if len(_data["members"]) > 0:
            doc["members"] = _data["members"]
            #Make sure that the did membership in the auth system is updated
            #correctly.
            set_did(did, [m["did"] for m in doc["members"]])

        #Make sure that the roles are setup correctly based on the new data. If
        #this throws an error, then the commit won't happen for the circle.
        verify_roles(doc["roles"], did)

    return doc

def rm(circle=None, **kwargs):
    """Removes a circle for this data custodian.

    .. warning: This also removes the *membership* for the circle and revokes
        any access grants that this circle has.

    Args:
        circle (str): name of the circle to remove.
    """
    dbid = f"circle/{circle}"
    cdid = None
    with databases.app[dbid] as doc:
        cdid = doc["did"]
        doc["_deleted"] = True
    rm_did(cdid)

def ls(circle=None, **kwargs):
    """Lists all the circles for this data custodian that match the filter.

    Args:
        circle (str): :func:`~fnmatch.fnmatch` pattern to filter circles by.

    Returns:
        dict: with structure that matches model `CircleCollection`.
    """
    viewres = []
    for idoc in get_view("circles", "circles_view").result:
        if fnmatch(idoc["id"], f"circle/{circle}"):
            with databases.app[idoc["id"]] as cdoc:
                viewres.append(cdoc)

    return {
        "circles": viewres
    }

_member_filter = {
    "dids": lambda m, f: m["did"] in f.get("dids", []),
    "aliases": lambda m, f: m["alias"] in f.get("aliases", []),
    "names": lambda m, f: m["name"] in f.get("names", []),
    "added_start": lambda m, f: m["added"] > f.get("added_start", 0),
    "added_end": lambda m, f: m["added"] < f.get("added_end", 1e300),
    "tags": lambda m, f: any(t in f.get("tags", []) for t in m["tags"])
}

def _filter_members(members, filters):
    """Filters the set of members to return only those that match the filters.

    Args:
        members (list): of `dict` that match the model `CircleMember`.
        filters (dict): that matches the model `CircleMemberFilter`.
    """
    result = []
    fkeys = list(filters.keys())
    for member in members:
        #Check all the filters for which values were actually supplied.
        keep = all(v(member, filters) for k, v in _member_filter.items()
                   if k in fkeys)
        if keep:
            result.append(member)
    return result

def search_members(circle=None, _data=None, **kwargs):
    """Searches all the members of a given circle.

    Args:
        circle (str): name of the circle to list members for.
        _data (dict): filter for the members. Follows the structure of the model
            `CircleMemberFilter`.

    Returns:
        dict: with structure that matches model `CircleMembership`.
    """
    assert circle is not None
    dbid = f"circle/{circle}"
    if _data is None or len(_data) == 0:
        #We are returning all the members of the circle.
        with databases.app[dbid] as doc:
            result = doc["members"]
        return {
            "name": circle,
            "members": result
        }

    else:
        #Filter the members based on their attributes.
        with databases.app[dbid] as doc:
            members = doc["members"]
        return {
            "name": circle,
            "members": _filter_members(members, _data)
        }

def add_members(circle=None, _data=None, **kwargs):
    """Adds members to the given circle.

    Args:
        circle (str): name of the circle to add members to.
        _data (dict): members to add from the request JSON; should follow the
            structure of the model `CircleMembership`.
    """
    assert circle is not None
    dbid = f"circle/{circle}"
    roles, cdid = None, None

    if _data is not None and len(_data) > 0:
        assert _data["circle"] == circle
        #We compile a list of the new members by did; then we know to add them
        #from this list if they already exist for the circle. Otherwise, we
        #just keep them in the existing list.
        ndids = {m["did"]: m for m in _data["members"]}
        with databases.app[dbid] as doc:
            mems = {}
            for member in doc.get("members", []):
                if member["did"] not in ndids:
                    mems[member["did"]] = member
                else:
                    mems[member["did"]] = ndids[member["did"]]

            for mdid, member in ndids.items():
                if mdid not in mems:
                    mems[mdid] = member

            doc["members"] = list(mems.values())
            roles = doc["roles"]
            cdid = doc["did"]
            #Update the DID's children in the roles/auth system.
            set_did(cdid, [m["did"] for m in doc["members"]])

        verify_roles(roles, cdid)

def rm_members(circle=None, _data=None, **kwargs):
    """Removes members from the given circle.

    Args:
        circle (str): name of the circle to remove members from.
        _data (dict): members to remove (from the request JSON); should follow
            the structure of the model `CircleMembership`. If empty `dict`, then
            remove *all* the members from the circle.
    """
    assert circle is not None
    dbid = f"circle/{circle}"
    roles, cdid = None, None

    if _data is None or len(_data) == 0:
        #We are removing *all* the members of the circle.
        with databases.app[dbid] as doc:
            del doc["members"]
            roles = doc["roles"]
            cdid = doc["did"]
            #Update the DID's children in the roles/auth system.
            set_did(cdid)
    else:
        #Remove only those members specified in the request.
        rdids = [m["did"] for m in _data["members"]]
        if len(rdids) == 0:
            return

        with databases.app[dbid] as doc:
            keep = []
            for member in doc.get("members", []):
                if member["did"] not in rdids:
                    keep.append(member)
            doc["members"] = keep
            roles = doc["roles"]
            cdid = doc["did"]
            #Update the DID's children in the roles/auth system.
            set_did(cdid, [m["did"] for m in doc["members"]])

    #Finally, verify the role assignments for the application again.
    verify_roles(roles, cdid)
