"""Provides clients and basic methods for interacting with the distributed
`couchdb`.
"""
import logging
from cloudant.client import CouchDB
from cloudant.document import Document as CouchDocument
from cloudant.design_document import DesignDocument
from cloudant.view import View
from cloudant.query import Query

from os import environ
from attrdict import AttrDict
from requests.adapters import HTTPAdapter

client = None
"""cloudant.client.CouchDB: database access client for `couchdb`.
"""
managed = None
"""list: of `str` database names that are managed by the `datacustodian`
application.
"""
databases = None
"""AttrDict: keys are database names; values are the :class:`Database` client
database instances retrieved by :data:`client`.
"""
package = None
"""str: name of the package that the databases are being configured for.
"""

log = logging.getLogger(__name__)


class Database(object):
    """Represents a connection to a `couchdb` database for convenience of working
    with documents from multiple databases.

    Args:
        db (cloudant.Database): database object to work with.
    """

    def __init__(self, db):
        self.db = db

    def __getitem__(self, doc_id):
        """Opens a context manager for document CRUD operations on the client.
        """
        return CouchDocument(self.db, doc_id)


def configure(packspec, url=None, norun=False, **couchargs):
    """Configures the `couchdb` client using the application specifications.

    Args:
        packspec (attrdict.AttrDict): package specifications for the overall application.
        url (str): URL that the `couchdb` API is served from.
    """
    assert url is not None
    global client, managed, package
    # Append the name of the package application databases to the list of managed
    # databases.
    package = packspec.name
    managed = [f"{package}_app", f"{package}_acl", f"{package}_fido"]
    system_dbs = ["_users", "_replicator"]

    # Configure an adapter so that multiple requests can be executed concurrently.
    adapter = {
        "pool_connections": couchargs.get("pool_connections", 10),
        "pool_maxsize": couchargs.get("pool_maxsize", 100)
    }
    log.debug(f"Configuring HTTP adapter using {adapter}.")
    http_adapter = HTTPAdapter(**adapter)
    # Make sure that the URL has the correct protocol specified.
    if "http" not in url:
        url = f"http://{url}"

    if norun:
        return

    client = CouchDB(environ["COUCHDB_USERNAME"],
                     environ["COUCHDB_PASSWORD"],
                     url=url,
                     connect=True,
                     adapter=http_adapter)

    session = client.session()
    log.info(f"Connected CouchDB at {url}.")
    log.debug(f"Username: {session['userCtx']['name']}")

    dbs = client.all_dbs()
    log.debug(f"Databases: {dbs}")

    # Make sure the system databases are being made for new installations.
    for dbname in system_dbs:
        if dbname not in client:
            log.debug(f"Creating system database {dbname}.")
            _db = client.create_database(dbname)

    # Create any missing databases in the client.
    global databases
    log.info(f"Initializing managed databases using {client}.")
    dbd = {}
    for dbname in managed:
        short_name = dbname.split('_')[-1]
        if dbname not in client:
            log.debug(f"Creating database {dbname}.")
            _db = client.create_database(dbname)
            dbd[short_name] = Database(_db)
        else:
            dbd[dbname] = Database(client[dbname])


    databases = AttrDict(dbd)

    # Next, configure the views and indices.
    configure_views()
    configure_indexes()


def cleanup():
    """Cleans up the database client connections.
    """
    global client
    if client is not None:
        client.disconnect()


_circles_views = {
    "circles_view": (0, """
    function (doc) {
        if (doc._id && doc._id.substring(0, 7) == "circle/") {
            emit(doc._id, doc.did);
        }
    }
    // version=0
    """)
}
"""dict: keys are view names for views needed by the :mod:`datacustodian.circles`.
Values are a `tuple` with `(version, mapfunc)`. The map function should include
a comment with `version={version}` so that `datacustodian` knows when to upgrade
the map/reduce functions.
"""
_consent_views = {
    "grant_view": (0, """
    // version=0
    function (doc) {
        if (doc.grants) {
            for (did in doc.grants) {
                did_url = doc.grants[did]["did_url"];
                emit(did_url, did);
            }
        }
        if (doc.issuance_history) {
            for (did in doc.issuance_history) {
                for (entry in doc.issuance_history[did]) {
                    did_url = entry["did_url"];
                    emit(did_url, did);
                }
            }
        }
        if (doc.revocation_history) {
            for (did in doc.revocation_history) {
                for (entry in doc.revocation_history[did]) {
                    did_url = entry["did_url"];
                    emit(did_url, did);
                }
            }
        }
    }
    """),
    "did_view": (0, """
    // version=0
    function (doc) {
        if (doc.grants) {
            for (did in doc.grants) {
                emit(did, "active");
            }
        }
        if (doc.issuance_history) {
            for (did in doc.issuance_history) {
                for (entry in doc.issuance_history[did]) {
                    emit(did, "issued");
                }
            }
        }
        if (doc.revocation_history) {
            for (did in doc.revocation_history) {
                for (entry in doc.revocation_history[did]) {
                    emit(did, "revoked");
                }
            }
        }
    }
    """)
}
"""dict: keys are index names needed by :mod:`datacustodian.consent` to manage
access-control and sharing. Values are a `tuple` with `(version, mapfunc)`.
The map function should include a comment with `version={version}` so that
`datacustodian` knows when to upgrade the map/reduce functions.
"""
_dlt_views = {
    "credentials_view": (0, """
    function (doc) {
        if (doc._id && doc.credential_definition_id) {
            emit(doc.credential_definition_id, doc.schema_id);
        }
    }
    // version=0
    """)
}
"""dict: keys are view names for views needed by the :mod:`datacustodian.dlt`.
Values are a `tuple` with `(version, mapfunc)`. The map function should include
a comment with `version={version}` so that `datacustodian` knows when to upgrade
the map/reduce functions.
"""
_fido_views = {
    "challenges_view": (0, """
    function (doc) {
        if (doc._id && doc.challenge) {
            emit(doc.challenge, doc._id);
        }
    }
    // version=0
    """)
}
"""dict: keys are view names for views needed by the :mod:`datacustodian.circles`.
Values are a `tuple` with `(version, mapfunc)`. The map function should include
a comment with `version={version}` so that `datacustodian` knows when to upgrade
the map/reduce functions.
"""
views = {
    "circles": (_circles_views, "app"),
    "consent": (_consent_views, "acl"),
    "dlt": (_dlt_views, "app"),
    "fido": (_fido_views, "fido")
}
"""dict: keys are module names; values are the view dictionaries.
"""
indexes = {
}
"""dict: keys are module names; values are the index dictionaries.
"""


def configure_indexes():
    """Sets up the indices in the `app` database if they don't already exist.
    """
    for module in indexes:
        _configure_index(module)


def configure_views():
    """Sets up the views in the `app` database if they don't already exist.
    """
    for module in views:
        _configure_view(module)


def _configure_index(module):
    """Sets up indices in the database for a module if they don't already exist.
    Manages index mapping function versions using the `tuple` in the index `dict`.

    Args:
        module (str): name of the module to configure the indexes for. Should be
            one of the keys in :data:`indexes`.
    """
    mod_index, dbname = indexes.get(module, ({}, "app"))
    _db = getattr(databases, dbname)
    with DesignDocument(_db.db, f"_design/{module}") as doc:
        _indexes = doc.list_indexes()
        for index_name, (version, search_func) in mod_index.items():
            if index_name not in _indexes:
                doc.add_search_index(index_name, search_func)
            else:
                indexdoc = doc.get_index(index_name)
                verstr = f"version={version}"
                if verstr not in indexdoc["index"]:
                    # The version of this index has been updated, we need to
                    # re-register it with the server.
                    doc.update_search_index(index_name, search_func)


def _configure_view(module):
    """Sets up the views in the database for one module, if they don't already
    exist. Manages versions using the tuple in the views `dict`.

    Args:
        module (str): name of the module to configure the views for. Should be
            one of the keys in :data:`views`.
    """
    # First, update the views. We'll use a separate context manager to create the
    # search indexes.
    mod_view, dbname = views.get(module, ({}, "app"))
    _db = getattr(databases, dbname)
    with DesignDocument(_db.db, f"_design/{module}") as doc:
        _views = doc.list_views()
        for view_name, (version, map_func) in mod_view.items():
            if view_name not in _views:
                doc.add_view(view_name, map_func)
            else:
                viewdoc = doc.get_view(view_name)
                verstr = f"version={version}"
                if verstr not in viewdoc["map"]:
                    # The version of this view has been updated, we need to
                    # re-register it with the server.
                    doc.update_view(view_name, map_func)


def get_query(module, selector, index_name):
    """Returns results from querying the index for the specified module.

    Args:
        module (str): name of the module that defines the index.
        selector (dict): selector query, see [1]_.
        index_name (str): name of the index to use to speed up the query.

    References:
        1_: https://docs.couchdb.org/en/stable/api/database/find.html#find-selectors
    """
    dbname = indexes[module][1]
    return Query(getattr(databases, dbname).db,
                 selector=selector,
                 use_index=index_name)


def get_view(module, view_name):
    """Return a view object to interact with a view on the db server.

    Args:
        module (str): name of the module to grab views for.
        view_name (str): name of the view to iterate over.
    """
    dbname = views[module][1]
    v = View(getattr(databases, dbname).db[f"_design/{module}"], view_name)
    return v
